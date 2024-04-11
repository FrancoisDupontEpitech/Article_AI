import spacy
import json

def open_json(json_path):
    with open(json_path, 'r', encoding='utf8') as file:
        return json.load(file)

def articles_to_json(articles, json_path):
    with open(json_path, 'w', encoding='utf8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)

def main():
    nlp = spacy.load("fr_core_news_sm")

    tokenized_articles = open_json("jsons/tokenized_articles.json")
    lemmatized_articles = {}

    for key, tokens in tokenized_articles.items():
        article_text = " ".join(tokens)
        doc = nlp(article_text)

        lemmatized_text = " ".join([token.lemma_ for token in doc if not token.is_punct and not token.is_space])
        lemmatized_articles[key] = lemmatized_text

    articles_to_json(lemmatized_articles, 'jsons/lemmatized_articles.json')

if __name__ == "__main__":
    main()
