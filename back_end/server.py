from flask import Flask
from database import connect_to_database
from web_scraper import *
app = Flask(__name__)

@app.route('/')
@app.route('/scrape_news_sources')
def scrape_news_sources():
    scraped_articles = []
    connection = connect_to_database()
    cyber_security_dive_list = [
    'https://www.cybersecuritydive.com/topic/breaches/', 'https://www.cybersecuritydive.com/topic/vulnerability/',
    'https://www.cybersecuritydive.com/topic/cyberattacks/', 'https://www.cybersecuritydive.com/topic/threats/'
    ]
    cyber_security_news_list = [
        'https://cybersecuritynews.com/category/threats/', 'https://cybersecuritynews.com/category/cyber-attack/', 
        'https://cybersecuritynews.com/category/vulnerability/', 'https://cybersecuritynews.com/category/data-breaches/'
        ]
    
    for url in cyber_security_dive_list:
        scrape_cyber_security_dive(url = url, prefix= url, data = scraped_articles, max_pages = 3, current_page=1)

    for url in cyber_security_news_list:
        scrape_cyber_security_news(url = url, data = scraped_articles, max_pages = 3, current_page=1)

    scrape_hacker_news(url = 'https://thehackernews.com/', data = scraped_articles, max_pages = 3, current_page=1)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)