import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def compute_grammar_score(text: str):
    matches = tool.check(text)

    num_words = len(text.split())
    num_errors = len(matches)
    errors_per_100 = (num_errors / num_words) * 100
    error_types = {}

    for match in matches:
        category = match.ruleIssueType
        error_types[category] = error_types.get(category, 0) + 1
    
    grammar_score = {}
    grammar_score["total_words"] = num_words
    grammar_score["total_errors"] = num_errors
    grammar_score["errors_per_100"] = errors_per_100
    grammar_score["error_types"] = error_types

    return grammar_score 




def main():
    text = """
Today I had a presentation in my class. I was very nervous, so I speak too fast and forget some words. But my teacher say I did well, and my friend clap for me. I think next time I will prepare more better.
    """

    grammar_score = compute_grammar_score(text)

    print("Total words:", grammar_score["total_words"])
    print("Total errors:", grammar_score["total_errors"])
    print("Errors per 100:", grammar_score["errors_per_100"])
    print("Error Types:", grammar_score["error_types"])

if __name__ == "__main__":
    main()
