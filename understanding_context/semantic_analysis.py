import gensim
from gensim import corpora
from gensim.models import LdaModel
import json

def load_cleaned_articles(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def prepare_documents(articles):
    return list(articles.values())

def build_lda_model(documents):
    dictionary = corpora.Dictionary(documents)
    corpus = [dictionary.doc2bow(doc) for doc in documents]
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, passes=15)
    return lda_model, dictionary, corpus

def print_topics(lda_model, dictionary):
    topics = lda_model.print_topics(num_words=4)
    for topic in topics:
        print(topic)

def main():
    cleaned_articles = load_cleaned_articles("jsons/cleaned_articles.json")
    documents = prepare_documents(cleaned_articles)
    lda_model, dictionary, corpus = build_lda_model(documents)
    print_topics(lda_model, dictionary)

if __name__ == "__main__":
    main()
