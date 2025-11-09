import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template

app = Flask(__name__)

def scrape_ai_news():
    url = 'https://techcrunch.com/tag/ai/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    articles = []
    # Search for all <a> tags that have "/202" in href (most TechCrunch articles)
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('https://techcrunch.com/20') and len(a.text.strip()) > 10:
            articles.append({'title': a.text.strip(), 'url': href})
            if len(articles) >= 3:
                break
    return articles

@app.route('/')
def home():
    return render_template('vc_index.html')


@app.route('/top-ai-news')
def top_ai_news():
    try:
        news = scrape_ai_news()
        return jsonify(news)
    except Exception as e:
        # Detailed error for debugging
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    # Use 0.0.0.0 to allow access from browser, port 5001.
    app.run(host="0.0.0.0", port=5001)