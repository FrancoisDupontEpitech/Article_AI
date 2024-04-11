import spacy
import fr_core_news_sm
import json

def load_language_model():
    return spacy.load("fr_core_news_sm")

def tokenize_text(nlp, text):
    doc = nlp(text)
    return [token.text for token in doc]

def tokenizer(articles):
    nlp = load_language_model()
    tokenized_articles = {}

    for url, text in articles.items():
        tokenized_text = tokenize_text(nlp, text)
        tokenized_articles[url] = tokenized_text

    with open("jsons/google_news/tokenized_articles.json", 'w', encoding='utf8') as file:
        json.dump(tokenized_articles, file, ensure_ascii=False, indent=4)

    return tokenized_articles