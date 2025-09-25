
import re
import nltk as nltk


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z]+", text.lower())

def tokenize_nltk(text: str) -> list[str]:
    return nltk.word_tokenize(text.lower())

