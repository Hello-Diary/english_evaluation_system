import spacy
from collections import Counter

# Load a spaCy English model
nlp = spacy.load("en_core_web_sm")

def analyze_sentence_variety(text: str):
    doc = nlp(text)
    total_sentences = 0
    complex_sentences = 0
    sub_clause_count = 0
    conjunctions = Counter()

    for sent in doc.sents:
        total_sentences += 1
        has_complexity = False

        for token in sent:
            # Relative clauses
            if token.dep_ == "relcl":
                has_complexity = True
                sub_clause_count += 1

            # Subordinating or coordinating conjunctions
            if token.pos_ in {"SCONJ", "CCONJ"}:
                conjunctions[token.text.lower()] += 1
                has_complexity = True

        if has_complexity:
            complex_sentences += 1

    return {
        "total_sentences": total_sentences,
        "complex_sentences": complex_sentences,
        "complex_sentence_ratio": round(complex_sentences / total_sentences, 3) if total_sentences else 0,
        "avg_subordinate_clauses_per_sentence": round(sub_clause_count / total_sentences, 3) if total_sentences else 0,
        "conjunction_frequencies": dict(conjunctions),
    }

def main():
# Example
    text = """
    I went to the park. I met my friend who was reading a book.
    She said she couldn’t stay long because she had homework.
    It was raining, but we still walked together.
    """

    results = analyze_sentence_variety(text)
    print(results)


if __name__ == "__main__":
    main()
