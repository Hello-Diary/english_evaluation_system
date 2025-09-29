import csv
from dataclasses import dataclass
import pandas as pd
import re

from services import tokenizer


# import nltk
# from nltk.tokenize import word_tokenize

# nltk.download("punkt")        # basic tokenizer
# nltk.download("punkt_tab")

@dataclass
class VocabLevel:
    a1_words: list[str]
    a2_words: list[str]
    b1_words: list[str]
    b2_words: list[str]
    c1_words: list[str]
    c2_words: list[str]
    unknown_words: list[str]
    error_words: list[str]

def load_oxford5000(filepath: str) -> dict[str,str]:
    word_levels = {}
    with open(filepath, mode="r", encoding="utf") as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row["word"].strip().lower()
            level = row["level"].strip().lower()
            word_levels[word] = level
    return word_levels


def load_oxford5000_pandas(filepath: str) -> dict[str,str]:
    df = pd.read_csv(filepath)
    df["word"] = df["word"].str.lower().str.strip()
    return dict(zip(df["word"],df["level"]))


def classify_word(word: str, word_levels: dict[str,str]) -> str:
    return word_levels.get(word,"UNKNOWN")

def analyze_vocab_level(text: str, word_levels: dict[str, str]) -> VocabLevel:
    tokens = tokenizer.tokenize(text)
    level_buckets = {
        "a1": [],
        "a2": [],
        "b1": [],
        "b2": [],
        "c1": [],
        "c2": [],
        "UNKNOWN": [],
        "ERROR": [],
    }

    for token in tokens:
        token_level = classify_word(token, word_levels)
        if token_level in level_buckets:
            level_buckets[token_level].append(token)
        else:
            level_buckets["ERROR"].append(token)

    return VocabLevel(
        a1_words=level_buckets["a1"],
        a2_words=level_buckets["a2"],
        b1_words=level_buckets["b1"],
        b2_words=level_buckets["b2"],
        c1_words=level_buckets["c1"],
        c2_words=level_buckets["c2"],
        unknown_words=level_buckets["UNKNOWN"],
        error_words=level_buckets["ERROR"],
    )

def main():
    world_levels_oxford = load_oxford5000("dataset/oxford-5k.csv")
    test_string = """
Today I had a presentation in my class. I was very nervous, so I speak too fast and forget some words. But my teacher say I did well, and my friend clap for me. I think next time I will prepare more better.
    """
    vocab_analysis = analyze_vocab_level(test_string, world_levels_oxford)
    hello_level = world_levels_oxford["teacher"]
    print(hello_level)
    print("Vocab Analysis Results:", vocab_analysis)

if __name__ == "__main__":
    main()
