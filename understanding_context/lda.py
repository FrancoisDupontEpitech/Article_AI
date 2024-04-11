import spacy
import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.corpora import Dictionary
import json

def load_raw_articles(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def preprocess_articles(articles):
    # Load the spaCy model
    nlp = spacy.load("fr_core_news_sm")
    preprocessed_articles = []

    for article in articles.values():
        # Process the article text with spaCy
        doc = nlp(article)
        # Tokenize, remove stopwords and perform lemmatization
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
        preprocessed_articles.append(tokens)

    return preprocessed_articles

def prepare_dictionary_corpus(preprocessed_articles):
    dictionary = Dictionary(preprocessed_articles)
    corpus = [dictionary.doc2bow(article) for article in preprocessed_articles]
    return dictionary, corpus

def train_lda_model(dictionary, corpus, num_topics=10):
    assert len(corpus) > 0, "Corpus is empty"
    assert len(dictionary) > 0, "Dictionary is empty"

    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)
    return lda

def main():
    raw_articles = load_raw_articles("jsons/lemmatized_articles.json")
    preprocessed_articles = preprocess_articles(raw_articles)
    dictionary, corpus = prepare_dictionary_corpus(preprocessed_articles)
    lda_model = train_lda_model(dictionary, corpus)

    for idx, topic in lda_model.print_topics(-1):
        print(f"Topic: {idx} \nWords: {topic}")

if __name__ == "__main__":
    main()
