import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

def get_google_scholar_links(query):
    with sync_playwright() as p:
        # Launch the browser in headful mode to see what's happening
        browser = p.chromium.launch(headless=True)  # Set headless=False to see the browser
        page = browser.new_page()

        # Build the Google Scholar search URL with the user's query
        url = f"https://scholar.google.com/scholar?q={query}"
        print(f"Google Scholar URL: {url}")
        page.goto(url)

        # Adaptation for potential consent button on Google Scholar, if exists
        # Example: Click consent if needed here

        extracted_links = []
        # Assuming each result is contained in a similar structure
        for i in range(1, 11):  # Adjust based on how many links you want to fetch
            # Adjusting the XPath to target Google Scholar's specific structure
            xpath_expression = f'//div[@id="gs_res_ccl_mid"]/div[@class="gs_r gs_or gs_scl"][{i}]/div[@class="gs_ri"]/h3/a'
            link_element = page.query_selector(f'xpath={xpath_expression}')
            if link_element:
                href = link_element.get_attribute('href')
                extracted_links.append(href)

        browser.close()
        return extracted_links


def get_article_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            potential_content_selectors = [
                'article',  # Standard article tag
                'main',  # Main tag, often contains the primary content
                'div[class*="content"]',  # Divs that include "content" in their class name
                'div.post',  # Common class name for article posts
                'div.article-content',  # Another common class name for articles
            ]

            for selector in potential_content_selectors:
                article_content = soup.select_one(selector)
                if article_content:
                    break

            if not article_content:
                # Fallback to selecting the largest <p> parent
                paragraphs = soup.find_all('p')
                largest_p = max(paragraphs, key=lambda p: len(p.text), default=None)
                article_content = largest_p.parent if largest_p else None

            if article_content:
                article_text = ' '.join(article_content.stripped_strings)
                return article_text
            else:
                print("No article content found on the webpage.")
                return None
        else:
            print("Failed to retrieve the webpage. Status Code:", response.status_code)
            return None
    except Exception as e:
        print("Error retrieving or processing the webpage:", str(e))
        return None


def get_google_scholar_data(query):
    links = get_google_scholar_links(query)  # Make sure this function returns a list of URLs
    if not links:
        print("No links found.")
        return []

    data = []

    for link in links:
        article_text = get_article_content(link)
        if article_text:
            data.append({
                'url': link,
                'text': article_text
            })

    return data