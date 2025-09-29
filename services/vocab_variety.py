from dataclasses import dataclass
from lexical_diversity import lex_div as ld

from services import tokenizer

@dataclass
class VocabVariety:
    mltd: float

def compute_type_token_ratio(tokens: list[str]) -> float:
    unique = len(set(tokens))
    total =len(tokens) 
    return  unique / total

def get_mtld(tokens: list[str]) -> VocabVariety:
    return VocabVariety(ld.mtld(tokens))




def main():
    test_string = """
Today I had a presentation in my class. I was very nervous, so I speak too fast and forget some words. But my teacher say I did well, and my friend clap for me. I think next time I will prepare more better.
    """
    test_list = tokenizer.tokenize_nltk(test_string)
    mtld = get_mtld(test_list)
    print("Measure of Textual Lexical Diversity: ", mtld.mltd)


if __name__ == "__main__":
    main()
