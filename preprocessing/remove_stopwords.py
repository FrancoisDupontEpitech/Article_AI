import spacy
import json
import re

def load_json(json_path):
    with open(json_path, 'r', encoding='utf8') as file:
        return json.load(file)

def preprocess_text(tokenized_text):
    if 'nlp' not in globals():
        global nlp
        nlp = spacy.load("fr_core_news_sm")

    processed_tokens = [re.sub(r'[^\w\s]', '', token.lower()) for token in tokenized_text]
    processed_tokens = [token for token in processed_tokens if token.strip()]
    filtered_tokens = [token for token in processed_tokens if token not in nlp.Defaults.stop_words and not token.isdigit()]

    return filtered_tokens

def main():
    tokenized_articles = load_json("jsons/tokenized_articles.json")
    cleaned_articles = {}

    for key, value in tokenized_articles.items():
        cleaned_text = preprocess_text(value)
        cleaned_articles[key] = cleaned_text

    with open("jsons/cleaned_articles.json", 'w',  encoding='utf8') as file:
        json.dump(cleaned_articles, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
