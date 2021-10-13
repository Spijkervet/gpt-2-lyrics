import os
import threading
import regex as re
import logging

from googletrans import Translator

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from tendo import singleton

from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer
)


from run_generation import generate
# device = os.environ.get('DEVICE', 'cpu')
# device = "cuda:0"
device = "cpu"
flavor_id = device + os.environ.get('INSTANCE', ':0')

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(filename=f"logs/{hash(flavor_id)}.log", level=logging.INFO)
logger = logging.getLogger(__name__)
me = singleton.SingleInstance(flavor_id=flavor_id)
app = FastAPI(title="GPT-2", version="0.1",)
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

lock = threading.RLock()

translator = Translator()

model_class = GPT2LMHeadModel
tokenizer_class = GPT2Tokenizer
model = model_class.from_pretrained("lyrics", torchscript=True)
tokenizer = tokenizer_class.from_pretrained("lyrics")
model = model.to(device)

class Prompt(BaseModel):
    prompt:str = Field(..., max_length=3000, title='Model prompt')
    length:int = Field(15, ge=1, le=1000, title='Number of tokens generated in each sample')
    temperature:float = Field(0.7, ge=0.0, le=1.0, title="Sampling temperature")
    language:str = Field("en", title='Language')
    num_samples:int = Field(1, ge=1, le=8, title='Number of samples generated')


@app.post("/gpt2_lyrics/")
def gen_sample(prompt: Prompt):
    with lock:
        r = {}
        if prompt.language != "en":
            prompt.prompt = translator.translate(prompt.prompt, src=prompt.language, dest="en").text

        prompt.prompt = "<|startoftext|>" + prompt.prompt
        repetition_penalty = 1.0
        samples = generate(device, model, tokenizer, prompt.prompt, prompt.length, temperature=prompt.temperature, num_return_sequences=prompt.num_samples, repetition_penalty=repetition_penalty)

        new_lyrics = []
        for l in samples:
            l = l.replace('<|startoftext|>', '')
            l = l.replace("<|endoftext|>", "")
            l = l.replace(prompt.prompt, "", 1)

            if prompt.language != "en":
                l = translator.translate(l, src="en", dest=prompt.language).text

            l = l.replace(" u ", " je ")
            l = l.replace("U ", "Je ")
            new_lyrics.append(l)

        r['lyrics'] = new_lyrics
        # print("OUTPUT", new_lyrics)
        return r

@app.get("/health")
def healthcheck():
    return True
