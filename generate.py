from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask.ext.jsonpify import jsonify

import gpt_2_simple as gpt2

app = Flask(__name__)
api = Api(app)

class Lyrics(Resource):
    def get(self):
        generated = gpt2.generate(sess)
        print(generated)
        return 'hi'


api.add_resource(Lyrics, '/lyrics')




if __name__ == '__main__':
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess)
    app.run(port='5002')

