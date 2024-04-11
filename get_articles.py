from colorama import Fore, Style
from newspaper import Article, Config
import json

def get_article_text(link):
    config = Config()
    config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    article = Article(link, config=config)

    try:
        article.download()
        article.parse()
        return article.title, article.text
    except Exception as e:
        print(f"Erreur lors de la récupération de l'article: {e}")
        return None, None

def scrape_articles(links):
    articles = {}

    for link in links[:10]:
        print(f"{Fore.GREEN}Scraping: {Style.RESET_ALL}{link}")
        try:
            article_title, article_text = get_article_text(link)
            if article_text is not None:
                articles[link] = {'title': article_title, 'text': article_text}
        except Exception as e:
            print(f"Error scraping article from {link}: {e}. Skipping...")
            articles[link] = {'title': 'Failed to retrieve article', 'text': ''}

    return articles


def get_article_content(links):
    articles = scrape_articles(links)
    return articles