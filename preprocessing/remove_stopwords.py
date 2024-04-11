import spacy
import json
import re

def load_json(json_path):
    with open(json_path, 'r', encoding='utf8') as file:
        return json.load(file)

def load_language_model():
    return spacy.load("fr_core_news_sm")

def preprocess_text(tokenized_text, nlp):
    processed_tokens = [re.sub(r'[^\w\s]', '', token.lower()) for token in tokenized_text]
    processed_tokens = [token for token in processed_tokens if token.strip()]
    filtered_tokens = [token for token in processed_tokens if token not in nlp.Defaults.stop_words and not token.isdigit()]

    return filtered_tokens

def remove_stopwords(tokenized_articles):
    print("Removing stopwords...")
    nlp = load_language_model()
    cleaned_articles = {}

    for url, article in tokenized_articles.items():
        # Correctly pass tokenized title and text to preprocess_text
        tokenized_title = preprocess_text(article['title'], nlp)
        tokenized_text = preprocess_text(article['text'], nlp)

        # Use the cleaned_articles dictionary for storing results
        cleaned_articles[url] = {
            'title': tokenized_title,
            'text': tokenized_text
        }

    with open("jsons/google_news/cleaned_articles.json", 'w', encoding='utf8') as file:
        json.dump(cleaned_articles, file, ensure_ascii=False, indent=4)

    return cleaned_articles