# GPT-2-Lyrics
This repository is designed to fine tune existing GPT-2 models on lyric datasets.

## Usage
To fine-tune a pre-trained GPT-2 medium model on lyrics, with all the lyrics in a file called `lyrics.txt`, use:
```
sh finetune.sh
```

To generate samples from the finetuned model, use:
```
sh generate.sh
```

## Server
You can spin up an inference server using:
```
uvicorn rest:app --reload --host 0.0.0.0
```