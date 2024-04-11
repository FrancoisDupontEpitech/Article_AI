from textblob import TextBlob
import json

def load_cleaned_articles(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def analyze_sentiment(articles):
    articles_with_sentiment = {}

    for url, article_tokens in articles.items():
        # Combine the tokenized article back into a single string
        article_text = " ".join(article_tokens)

        # Use TextBlob for sentiment analysis
        blob = TextBlob(article_text)
        sentiment = blob.sentiment

        # Store the sentiment analysis result
        articles_with_sentiment[url] = {
            "polarity": sentiment.polarity,
            "subjectivity": sentiment.subjectivity
        }

    return articles_with_sentiment

def save_sentiment_analysis(articles_with_sentiment, json_path='articles_with_sentiment.json'):
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(articles_with_sentiment, file, ensure_ascii=False, indent=4)

def main():
    cleaned_articles = load_cleaned_articles("cleaned_articles.json")
    articles_with_sentiment = analyze_sentiment(cleaned_articles)
    save_sentiment_analysis(articles_with_sentiment)

if __name__ == "__main__":
    main()