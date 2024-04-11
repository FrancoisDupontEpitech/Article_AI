from transformers import pipeline, BartTokenizer
import json

def open_json(json_path):
    """Load articles from a JSON file."""
    with open(json_path, 'r', encoding='utf8') as file:
        return json.load(file)

def articles_to_json(articles, json_path):
    """Save article summaries to a JSON file."""
    with open(json_path, 'w', encoding='utf8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)

def summarize_article(text, summarizer, tokenizer, max_input_length=1024):
    # Tokenize the input text
    tokens = tokenizer.tokenize(text)

    # Truncate the tokens if necessary
    if len(tokens) > max_input_length:
        tokens = tokens[:max_input_length]

    # Convert tokens back to string
    truncated_text = tokenizer.convert_tokens_to_string(tokens)

    try:
        # Generate a summary
        summary = summarizer(truncated_text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Error generating summary."

def main():
    # Load the articles
    articles = open_json("jsons/articles.json")

    # Initialize the tokenizer and summarization pipeline
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Generate summaries for each article
    summaries = {url: summarize_article(text, summarizer, tokenizer) for url, text in articles.items()}

    # Save the summaries to a new JSON file
    articles_to_json(summaries, 'jsons/summarized_articles.json')

if __name__ == "__main__":
    main()
