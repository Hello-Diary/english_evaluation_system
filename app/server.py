from concurrent import futures
import grpc

from services import grammar_eval, sentence_variety, vocab_level, vocab_variety, tokenizer
from proto import analysis_pb2  # type: ignore
from proto import analysis_pb2_grpc  # type: ignore
# Preload Oxford 5000 dataset once at server startup
WORD_LEVELS = vocab_level.load_oxford5000("dataset/oxford-5k.csv")


class TextAnalysisService(analysis_pb2_grpc.TextAnalysisServicer):
    def AnalyzeText(self, request, context):
        text: str = request.text

        grammar = grammar_eval.compute_grammar_score(text)
        sentences = sentence_variety.analyze_sentence_variety(text)
        vocab = vocab_level.analyze_vocab_level(text, WORD_LEVELS)
        variety = vocab_variety.get_mtld(tokenizer.tokenize_nltk(text))

        return analysis_pb2.AnalysisResponse(
            grammar_score=analysis_pb2.GrammarScoreResponse(
                num_words=grammar.num_words,
                num_errors=grammar.num_errors,
                errors_per_100=grammar.errors_per_100,
                error_types=grammar.error_types,
            ),
            sentence_variety=analysis_pb2.SentenceVarietyResponse(
                total_sentences=sentences.total_sentences,
                complex_sentences=sentences.complex_sentences,
                complex_sentence_ratio=sentences.complex_sentence_ratio,
                avg_subordinate_clauses_per_sentence=sentences.avg_subordinate_clauses_per_sentence,
                conjunction_frequencies=sentences.conjunction_frequencies,
            ),
            vocab_level=analysis_pb2.VocabLevelResponse(
                a1_count=len(vocab.a1_words),
                a2_count=len(vocab.a2_words),
                b1_count=len(vocab.b1_words),
                b2_count=len(vocab.b2_words),
                c1_count=len(vocab.c1_words),
                c2_count=len(vocab.c2_words),
                unknown_count=len(vocab.unknown_words),
            ),
            vocab_variety=analysis_pb2.VocabVarietyResponse(
                mtld=variety.mtld,
            ),
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    analysis_pb2_grpc.add_TextAnalysisServicer_to_server(
        TextAnalysisService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
