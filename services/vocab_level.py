import csv
import pandas as pd
import re

from services import tokenizer


# import nltk
# from nltk.tokenize import word_tokenize

# nltk.download("punkt")        # basic tokenizer
# nltk.download("punkt_tab")

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

def analyze_vocab_level(text: str, word_levels: dict[str,str]) -> dict[str,list[str]]:
    tokens = tokenizer.tokenize(text)
    a1_tokens  = []
    b1_tokens  = []
    c1_tokens  = []
    unknown_tokens = []
    error_tokens = []
    for token in tokens:
        token_level = classify_word(token, word_levels)
        match token_level:
            case "a1":
                a1_tokens.append(token)
            case "b1":
                b1_tokens.append(token)
            case "c1":
                c1_tokens.append(token)
            case "UNKNOWN":
                unknown_tokens.append(token)
            case _:
                error_tokens.append(token)

    vocab_analysis = {
        "a1_count" : a1_tokens,
        "b1_count" : b1_tokens,
        "c1_count" : c1_tokens,
        "unknown_count" : unknown_tokens,
        "error_count" : error_tokens,
    }
    return vocab_analysis

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
