from playwright.sync_api import sync_playwright
from get_articles import get_article_content
from utils.write_to_json import write_to_json
from colorama import Fore, Style

def get_google_search_links(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = f"https://www.google.com/search?q={query}"
        print(f"url google news: {url}")
        page.goto(url)

        print("Page chargée OK")

        consent_button_xpath = '//*[@id="L2AGLb"]/div'
        page.wait_for_selector(f'xpath={consent_button_xpath}')
        print("Clique sur le bouton de consentement aux cookies...")
        page.click(f'xpath={consent_button_xpath}')

        page.wait_for_timeout(3000)
        print("Cookies acceptés")

        extracted_links = []
        for i in range(1, 11): # Pour extraire les 10 premiers liens
            xpath_expression = f'//*[@id="rso"]/div[{i}]/div/div/div[1]/div/div/span/a'
            link_elements = page.query_selector_all(f'xpath={xpath_expression}')
            for element in link_elements:
                href = element.get_attribute('href')
                extracted_links.append(href)

        browser.close()
        return extracted_links

def get_google_search_data(query):
    print(f"{Fore.MAGENTA}Getting Google SEARCH data: {Style.RESET_ALL}")
    links = get_google_search_links(query)
    if not links:
        print("No links found.")
        return []

    directory = "jsons/google_search/"

    write_to_json(links, f"{directory}links.json")
    articles = get_article_content(links)
    write_to_json(articles, f"{directory}articles.json")

    return articles
