import yfinance as yf
from bs4 import BeautifulSoup
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tkinter as tk
from tkinter import scrolledtext

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Functions for stock and sentiment
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

# GUI Function
def fetch_data():
    ticker = entry.get().upper()
    if not ticker:
        output_box.insert(tk.END, "Please enter a ticker symbol.\n")
        return

    try:
        output_box.delete(1.0, tk.END)  # Clear previous text
        stock_info = get_stock_info(ticker)
        news_sentiments = get_news_sentiment(ticker)
        sentiment_summary = classify_sentiment(news_sentiments)

        output_box.insert(tk.END, f"{stock_info}\n\nTop News Headlines & Sentiments:\n")
        for title, score in news_sentiments:
            output_box.insert(tk.END, f"Headline: {title}\nSentiment Score: {score:.2f}\n\n")
        output_box.insert(tk.END, f"Overall Sentiment: {sentiment_summary}\n")

    except Exception as e:
        output_box.insert(tk.END, f"Error fetching data: {e}\n")

# GUI setup
root = tk.Tk()
root.title("Stock Info & Sentiment Analyzer")

tk.Label(root, text="Enter Stock Ticker Symbol:").pack(pady=5)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

tk.Button(root, text="Get Info", command=fetch_data).pack(pady=5)

output_box = scrolledtext.ScrolledText(root, width=80, height=20)
output_box.pack(padx=10, pady=10)

root.mainloop()
