import json
from newspaper import Article, Config
from get_google_news_data import get_google_news_data
from get_google_scholar_data import get_google_scholar_data
from get_google_search_data import get_google_search_data
from utils.write_to_json import write_to_json
from preprocessing.tokenizer import tokenizer
from preprocessing.remove_stopwords import remove_stopwords
from preprocessing.lemmatizer import lemmatizer
from understanding_context.ner import ner

def get_article_text(link):
    config = Config()
    config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    article = Article(link, config=config)

    try:
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Erreur lors de la récupération de l'article: {e}")
        return None

def get_datasets(query):

    directory = "jsons/dataset/"

    datasets = []

    datasets.append(get_google_news_data(query))
    # datasets.append(get_google_scholar_data(query))     # marche pas (trop long et compliqué à scraper)
    datasets.append(get_google_search_data(query))

    write_to_json(datasets[0], directory + "dataset_1.json")
    # write_to_json(dataset_2, directory + "dataset_2.json")    # marche pas (trop long et compliqué à scraper)
    write_to_json(datasets[1], directory + "dataset_3.json")

    return datasets


def open_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except UnicodeDecodeError as e:
        print(f"Error decoding JSON file: {e}")
        return None
    except Exception as e:
        print(f"Error opening JSON file: {e}")
        return None

def preprocess(datasets):
    print("Prétraitement des données")

    preprocessed_datasets = []

    if datasets:
        for dataset in datasets:
            dataset_tokenizer = tokenizer(dataset)
            dataset_stopword = remove_stopwords(dataset_tokenizer)
            dataset_lemmatizer = lemmatizer(dataset_stopword)
            preprocessed_datasets.append(dataset_lemmatizer)

    else:
        print("No dataset available for tokenization.")
        return None

    return preprocessed_datasets


def analysis_and_processing(preprocessed_datasets):
    print("Analyse et traitement du contenu")

    analysised_datasets = []

    if preprocessed_datasets:
        for dataset in preprocessed_datasets:
            # OK - Extraction d'entités nommées (NER)
            dataset_ner = ner(dataset)
            # KO - Résumé de texte
            # dataset_summarized = summarize(dataset_ner)
            analysised_datasets.append(dataset_ner)

    else:
        print("No dataset available for tokenization.")
        return None

    return analysised_datasets

def main():
    print("Article AI")

    # query = input("Entrez votre recherche: ")
    # datasets = get_datasets(query)

    datasets = []
    datasets.append(open_json("jsons/dataset/dataset_1.json"))

    preprocessed_datasets = preprocess(datasets)
    datasets = analysis_and_processing(preprocessed_datasets)



    print("Les articles ont été récupérés")

if __name__ == "__main__":
    main()
