import requests
import time
from bs4 import BeautifulSoup

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
            print(series_list)
    
    return series_list
