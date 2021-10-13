import numpy as np
from glob import glob
from tqdm import tqdm


def format_punctuation(l):
    l = l.replace("-", "")
    l = l.replace(".", " . ")
    l = l.replace(",", " , ")
    l = l.replace(";", " ; ")
    l = l.replace(":", " : ")
    l = l.replace("!", " ! ")
    l = l.replace("?", " ? ")
    return l

def write_lyrics(fp, lyrics):
    with open(fp, "w") as f:
        f.write("\n\n".join(lyrics))

if __name__ == "__main__":
    lyrics = []
    for f in tqdm(glob("txt/*")):
        with open(f, "r") as f:
            lines = f.read()
            lines = format_punctuation(lines)

        lyrics.append(lines)

    mean_tokens = np.mean([len(l.split()) for l in lyrics])
    print("Mean tokens:", mean_tokens)
    print("Num examples:", len(lyrics))

    train_percentage = int(len(lyrics) * 0.9)
    train_lyrics = lyrics[:train_percentage]
    eval_lyrics = lyrics[train_percentage:]

    write_lyrics("train.txt", train_lyrics)
    write_lyrics("eval.txt", eval_lyrics)
