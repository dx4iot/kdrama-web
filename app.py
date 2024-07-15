from flask import Flask, render_template, request
from scrap import scrape_search_results  # Assuming your scraping function is in scraper.py

app = Flask(__name__)

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
