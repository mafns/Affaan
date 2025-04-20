import yfinance as yf
from bs4 import BeautifulSoup
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return f"{info['shortName']} ({ticker.upper()}) is trading at ${info['currentPrice']}."

def get_news_sentiment(query):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://duckduckgo.com/html/?q={query}+stock+news"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    results = soup.find_all('a', class_='result__a', limit=5)
    sentiments = []

    for result in results:
        headline = result.get_text()
        score = analyzer.polarity_scores(headline)['compound']
        sentiments.append((headline, score))

    return sentiments

def classify_sentiment(scores):
    avg = sum(score for _, score in scores) / len(scores)
    if avg > 0.2:
        return "Bullish"
    elif avg < -0.2:
        return "Bearish"
    else:
        return "Neutral"

# Example usage
ticker = "AAPL"
print(get_stock_info(ticker))
news = get_news_sentiment("Apple Inc")
for title, score in news:
    print(f"Headline: {title} | Sentiment Score: {score:.2f}")
print("Overall Sentiment:", classify_sentiment(news))
