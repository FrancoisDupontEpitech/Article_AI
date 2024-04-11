import spacy
import fr_core_news_sm
import json

def load_language_model():
    return spacy.load("fr_core_news_sm")

def tokenize_text(nlp, text):
    doc = nlp(text)
    return [token.text for token in doc]

def tokenizer(articles):
    print("Tokenizing articles...")
    nlp = load_language_model()
    tokenized_articles = {}

    for url, article in articles.items():
        # Tokenize both the title and the text of the article
        tokenized_title = tokenize_text(nlp, article['title'])
        tokenized_text = tokenize_text(nlp, article['text'])

        # Store them in a nested dictionary under the article's URL
        tokenized_articles[url] = {
            'title': tokenized_title,
            'text': tokenized_text
        }

    with open("jsons/google_news/tokenized_articles.json", 'w', encoding='utf8') as file:
        json.dump(tokenized_articles, file, ensure_ascii=False, indent=4)

    return tokenized_articles
