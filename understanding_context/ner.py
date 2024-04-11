import spacy
import json

def load_cleaned_articles(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_entities(articles):
    nlp = spacy.load("fr_core_news_sm")
    articles_with_entities = {}

    for url, article_tokens in articles.items():
        article_text = " ".join(article_tokens)
        doc = nlp(article_text)
        entities = []
        for ent in doc.ents:
            entities.append((ent.text, ent.label_))
        articles_with_entities[url] = entities

    return articles_with_entities

def save_entities(articles_with_entities, json_path='jsons/articles_with_entities.json'):
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(articles_with_entities, file, ensure_ascii=False, indent=4)

def main():
    cleaned_articles = load_cleaned_articles("jsons/articles.json")
    articles_with_entities = extract_entities(cleaned_articles)
    save_entities(articles_with_entities)

if __name__ == "__main__":
    main()
