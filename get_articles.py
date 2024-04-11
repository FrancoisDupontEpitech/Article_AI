from colorama import Fore, Style
from newspaper import Article, Config
import json

# def open_json(json_path):
#     try:
#         with open(json_path, 'r', encoding='utf-8') as file:
#             return json.load(file)
#     except UnicodeDecodeError as e:
#         print(f"Error decoding JSON file: {e}")
#         return None
#     except Exception as e:
#         print(f"Error opening JSON file: {e}")
#         return None

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

def scrape_articles(links):
    articles = {}

    for link in links[:10]:  # Limiting to 5 for testing, you can remove this limit
        print(f"{Fore.GREEN}Scraping: {Style.RESET_ALL}{link}")
        try:
            article_text = get_article_text(link)
            if article_text is not None:
                articles[link] = article_text
        except Exception as e:
            print(f"Error scraping article from {link}: {e}. Skipping...")
            articles[link] = "Failed to retrieve article."

    return articles


def get_article_content(links):
    # json_data = open_json('jsons/google_news.json')
    # links = [news_item['link'] for news_item in json_data['news']]
    articles = scrape_articles(links)
    return articles