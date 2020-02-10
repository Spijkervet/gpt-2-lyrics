from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from json import dumps

from celery import Celery
from celery.utils.log import get_task_logger
from celery.signals import worker_init, worker_process_init

import celery

import gpt_2_simple as gpt2

app = Flask(__name__)
# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
CORS(app)

sess = None

@worker_process_init.connect()
def on_worker_init(**_):
    global sess
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess)

@celery.task
def get_lyric(prefix, temperature, words):
    lyrics = gpt2.generate(sess, prefix=prefix, temperature=temperature, nsamples=8, length=words, batch_size=8, return_as_list=True,
        truncate="<|endoftext|>", include_prefix=False)
    return lyrics

@app.route('/', methods=['GET', 'POST'])
def index():
    data = request.get_json(force=True)
    prefix = data['lyrics'].strip()
    temperature = data['temperature']
    words = data['words']
    j = {}
    lyric = get_lyric.apply_async(args=[prefix, temperature, words]).get()
    lyric = [l[l.find(prefix)+len(prefix):] for l in lyric]
    lyric = [l.replace('<|startoftext|>', '') for l in lyric]
    j['lyrics'] = lyric
    return jsonify(j)

if __name__ == '__main__':
    app.run(port='5002')

