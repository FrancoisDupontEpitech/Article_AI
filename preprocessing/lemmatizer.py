import spacy
import json

# def open_json(json_path):
#     with open(json_path, 'r', encoding='utf8') as file:
#         return json.load(file)

def load_language_model():
    return spacy.load("fr_core_news_sm")

def lemmatize_text(nlp, tokens):
    article_text = " ".join(tokens)
    doc = nlp(article_text)
    return " ".join([token.lemma_ for token in doc if not token.is_punct and not token.is_space])

def lemmatizer(tokenized_articles):
    print("Lemmatizing articles...")
    if tokenized_articles is None:
        print("Error: tokenized_articles is None.")
        return None

    nlp = load_language_model()
    lemmatized_articles = {}

    for url, article in tokenized_articles.items():
        # Check if the article structure includes both title and text
        if 'title' in article and 'text' in article:
            lemmatized_title = lemmatize_text(nlp, article['title'])
            lemmatized_text = lemmatize_text(nlp, article['text'])
            lemmatized_articles[url] = {
                'title': lemmatized_title,
                'text': lemmatized_text
            }
        else:
            print(f"Skipping article {url} due to unexpected structure.")

    with open("jsons/google_news/lemmatized_articles.json", 'w', encoding='utf8') as file:
        json.dump(lemmatized_articles, file, ensure_ascii=False, indent=4)

    return lemmatized_articles
