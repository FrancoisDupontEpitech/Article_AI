from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import json

def open_json(json_path):
    with open(json_path, 'r') as file:
        return json.load(file)

def summarize_text(text, max_sentences):
    parser = PlaintextParser.from_string(text, Tokenizer("french"))
    summarizer = LexRankSummarizer()

    # Summarize to the desired number of sentences
    summary = summarizer(parser.document, sentences_count=max_sentences)

    # Combine sentences into a single string
    summarized_text = " ".join(str(sentence) for sentence in summary)

    return summarized_text

def summarize_articles(json_data, max_tokens):
    summarized_articles = {}

    for url, article_text in json_data.items():
        summarized_articles[url] = summarize_text(article_text, max_tokens)

    return summarized_articles

def main():
    json_data = open_json("articles.json")
    max_sentences = 50  # Adjust this value to control the length of the summary
    summarized_articles = summarize_articles(json_data, max_sentences)

    # Print or do whatever you want with the summarized articles
    for url, summary in summarized_articles.items():
        print("URL:", url)
        print("Summary:", summary)
        print()

if __name__ == "__main__":
    main()
