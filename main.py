from flask import Flask, render_template
import requests
from textblob import TextBlob
from collections import Counter
import json
import schedule
import threading
import time

app = Flask(__name__)

NEWS_API_KEY = 'hidden'
JSON_FILE_PATH = 'headlines.json'
LAST_UPDATE_TIME = None

def fetch_and_update_headlines():
    global LAST_UPDATE_TIME
    # Get news articles from News API
    news_url = f'https://newsapi.org/v2/everything?q=Elon%20Musk&apiKey={NEWS_API_KEY}'
    response = requests.get(news_url)
    articles = response.json().get('articles', [])

    # Extract headlines and perform sentiment analysis
    headlines_for_wordcloud = [article.get('title', '') for article in articles]
    combined_titles = ' '.join(headlines_for_wordcloud)

    # Split the string into words
    words = combined_titles.split()

    # Create a dictionary with word frequencies
    word_frequency_dict = Counter(words)

    # Save the headlines and word frequency data to a JSON file
    with open(JSON_FILE_PATH, 'w') as json_file:
        json.dump({
            'headlines': headlines_for_wordcloud,
            'word_frequency': word_frequency_dict
        }, json_file)

    LAST_UPDATE_TIME = time.strftime("%Y-%m-%d %H:%M:%S")
    print('Headlines updated and stored.')

def load_headlines_from_json():
    try:
        # Load headlines and word frequency data from the JSON file
        with open(JSON_FILE_PATH, 'r') as json_file:
            data = json.load(json_file)
        
        headlines_for_wordcloud = data.get('headlines', [])
        word_frequency_dict = data.get('word_frequency', {})

    except FileNotFoundError:
        headlines_for_wordcloud = []
        word_frequency_dict = {}

    return headlines_for_wordcloud, word_frequency_dict

@app.route('/')
def index():
    global LAST_UPDATE_TIME

    headlines_for_wordcloud, word_frequency_dict = load_headlines_from_json()

    # If there are no headlines in the JSON file or if it's time for an update, fetch and update headlines
    if not headlines_for_wordcloud or LAST_UPDATE_TIME is None or time.time() - time.mktime(time.strptime(LAST_UPDATE_TIME, "%Y-%m-%d %H:%M:%S")) > 24 * 60 * 60:
        fetch_and_update_headlines()
        headlines_for_wordcloud, word_frequency_dict = load_headlines_from_json()

    # Perform sentiment analysis using TextBlob
    positive_headlines = sum(TextBlob(headline).sentiment.polarity > 0 for headline in headlines_for_wordcloud)

    # Calculate the percentage of positive headlines
    total_headlines = len(headlines_for_wordcloud)
    positive_percentage = (positive_headlines / total_headlines) * 100 if total_headlines > 0 else 0
    formatted_percentage = "{:.2f}".format(positive_percentage)

    # Calculate the time remaining until the next update
    next_update_time = time.mktime(time.strptime(LAST_UPDATE_TIME, "%Y-%m-%d %H:%M:%S")) + 24 * 60 * 60
    time_remaining = max(0, next_update_time - time.time())

    # Convert time_remaining to hours and minutes
    hours, remainder = divmod(time_remaining, 3600)
    minutes, _ = divmod(remainder, 60)

    return render_template('index.html', positive_percentage=formatted_percentage, wordFrequencyData=json.dumps(word_frequency_dict), lastUpdateTime=LAST_UPDATE_TIME, timeRemainingHours=hours, timeRemainingMinutes=minutes)

# Run the scheduler in a separate thread
if __name__ == '__main__':
    # Run the scheduler in a separate thread
    schedule_thread = threading.Thread(target=lambda: schedule.run_pending(), daemon=True)
    schedule_thread.start()

    # Run the Flask app in debug mode
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
