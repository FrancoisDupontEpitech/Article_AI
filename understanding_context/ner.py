import spacy
import json

def extract_entities(articles):
    nlp = spacy.load("fr_core_news_sm")
    articles_with_entities = {}

    for url, article in articles.items():
        article_text = article['title'] + " " + article['text']  # Concatenate title and text for NER
        doc = nlp(article_text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        articles_with_entities[url] = entities

    return articles_with_entities

def ner(articles):
    print("Extraction des entités nommées (NER)...")
    articles_with_entities = extract_entities(articles)

    with open("jsons/google_news/articles_with_entities.json", 'w', encoding='utf8') as file:
        json.dump(articles_with_entities, file, ensure_ascii=False, indent=4)

    return articles_with_entities
