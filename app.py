from flask import Flask, render_template, request
import requests
import time
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_search_results(query):
    base_url = "https://kd.rohi.dev/search?q="
    url = base_url + query

    retries = 3  # Number of retry attempts
    delay = 1  # Initial delay in seconds

    for attempt in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            break
        else:
            time.sleep(delay)
            delay *= 2  # Exponential backoff

    if response.status_code != 200:
        return None  # Handle the error gracefully in your web app

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Extract search results
    results = soup.find_all('h3')
    img_tags = soup.find_all('img')
    a_tags = soup.find_all('a', href=lambda href: href and href.startswith('/drama/'))
    
    series_list = []
    
    # Extract titles, image URLs, and full URLs
    for i in range(min(len(results), len(img_tags), len(a_tags))):
        title = results[i].text.strip()
        img_url = img_tags[i]['src']
        href = a_tags[i]['href']
        base_url_new = "https://kd.rohi.dev/"
        # Filter image URLs starting with "https://asianimg.pro"
        if img_url.startswith("https://asianimg.pro"):
            full_url = base_url_new + href
            series_list.append({'title': title, 'img_url': img_url, 'full_url': full_url})
    
    return series_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    series_list = scrape_search_results(query)
    return render_template('results.html', series_list=series_list)

if __name__ == '__main__':
    app.run(debug=True)
