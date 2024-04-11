from playwright.sync_api import sync_playwright
from get_articles import get_article_content
from utils.write_to_json import write_to_json
from colorama import Fore, Style
import requests

def get_final_redirect(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.url
    except Exception as e:
        print("Error retrieving or processing the URL:", str(e))
        return None

def get_google_news_links(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = f"https://news.google.com/search?q={query}&hl=fr&gl=FR&ceid=FR%3Afr"
        print(f"url google news: {url}")
        page.goto(url)

        print("Page chargée OK")

        consent_button_xpath = '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/div[3]'
        page.wait_for_selector(f'xpath={consent_button_xpath}')
        print("Clique sur le bouton de consentement aux cookies...")
        page.click(f'xpath={consent_button_xpath}')

        page.wait_for_timeout(3000)
        print("Cookies acceptés")

        extracted_links = []
        for i in range(1, 11): # Pour extraire les 10 premiers liens
            xpath_expression = f'//*[@id="yDmH0d"]/c-wiz/div/main/div[2]/c-wiz/c-wiz[{i}]/c-wiz/article/div[1]/div[1]/a'
            link_elements = page.query_selector_all(f'xpath={xpath_expression}')
            for element in link_elements:
                href = element.get_attribute('href')
                if href.startswith('./'):
                    # Convertir le chemin relatif en URL absolue
                    full_url = f"https://news.google.com{href[1:]}"
                    extracted_links.append(full_url)
                else:
                    extracted_links.append(href)

        browser.close()
        return extracted_links

def get_google_news_data(query):
    print(f"{Fore.MAGENTA}Getting Google NEWS data: {Style.RESET_ALL}")
    links = get_google_news_links(query)
    if not links:
        print("No links found.")
        return []

    final_links = [get_final_redirect(link) for link in links]
    final_links = [link for link in final_links if link]  # Remove None values

    directory = "jsons/google_news/"

    write_to_json(final_links, f"{directory}links.json")
    articles = get_article_content(final_links)
    write_to_json(articles, f"{directory}articles.json")

    return articles
