import language_tool_python
from dataclasses import dataclass

tool = language_tool_python.LanguageTool('en-US')

@dataclass
class GrammarScore:
    num_words: int
    num_errors: int
    errors_per_100: float
    error_types: dict[str, int]

    def summary(self) -> str:
        return (
            f"Words: {self.num_words}, Errors: {self.num_errors}, "
            f"Errors per 100: {self.errors_per_100:.2f}, "
            f"Error Types: {self.error_types}"
        )

def compute_grammar_score(text: str)-> GrammarScore:
    matches = tool.check(text)

    num_words = len(text.split())
    num_errors = len(matches)
    errors_per_100 = (num_errors / num_words) * 100
    error_types:    dict[str,int] = {}

    for match in matches:
        category = match.ruleIssueType
        error_types[category] = error_types.get(category, 0) + 1
    
    return GrammarScore(
        num_words=num_words,
        num_errors=num_errors,
        errors_per_100=errors_per_100,
        error_types=error_types,
    )



def main():
    text = """
Today I had a presentation in my class. I was very nervous, so I speak too fast and forget some words. But my teacher say I did well, and my friend clap for me. I think next time I will prepare more better.
    """

    grammar_score = compute_grammar_score(text)
    print(grammar_score.summary())

if __name__ == "__main__":
    main()
