from flask import Flask
from flask_cors import cross_origin
from database import connect_to_database, insert_articles, retrieve_articles, retrive_analytics
from web_scraper import scrape_cyber_security_dive, scrape_cyber_security_news, scrape_hacker_news
from classification import extract_cves, extract_tags, remove_punctuation, determine_severity
import random
import json
app = Flask(__name__)

@app.route('/scrape_news_sources')
def scrape_news_sources():
    scraped_articles = []
    database_connection = connect_to_database()
    if database_connection:
        cyber_security_dive_list = [
        'https://www.cybersecuritydive.com/topic/breaches/', 'https://www.cybersecuritydive.com/topic/vulnerability/',
        'https://www.cybersecuritydive.com/topic/cyberattacks/', 'https://www.cybersecuritydive.com/topic/threats/']

        cyber_security_news_list = [
            'https://cybersecuritynews.com/category/threats/', 'https://cybersecuritynews.com/category/cyber-attack/', 
            'https://cybersecuritynews.com/category/vulnerability/', 'https://cybersecuritynews.com/category/data-breaches/']
        
        hacker_news_urls = ["https://thehackernews.com/","https://thehackernews.com/search/label/data%20breach",
                    "https://thehackernews.com/search/label/Cyber%20Attack", "https://thehackernews.com/search/label/Vulnerability"]
        
        for url in cyber_security_dive_list:
            scrape_cyber_security_dive(url = url, prefix= url, data = scraped_articles, max_pages = 3, current_page=1)

        for url in cyber_security_news_list:
            scrape_cyber_security_news(url = url, data = scraped_articles, max_pages = 3, current_page=1)

        for url in hacker_news_urls:
            scrape_hacker_news(url = url, data = scraped_articles, max_pages = 3, current_page=1)

        verified_articles = []
        for article in scraped_articles:
            CVES = extract_cves(title = article['title'], text = article['description'])
            article['tags'] = extract_tags(title = article['title'], text = article['description'], matched_tags= article['tags'])
            article['severity'] = determine_severity(tags = article['tags'], cves= CVES)
            for cve in CVES:
                article['tags'].append(cve)
            
            if article['tags']:
                verified_articles.append(article)
        
        random.shuffle(verified_articles)
        insert_articles(articles=verified_articles, connection = connect_to_database())

        return ("Scraping Successful", 200)
    return ("Scraping Unsuccessful", 500)

@app.route('/fetch_articles/<offset>/<limit>')
@cross_origin()
def fetch_articles(offset: int, limit: int) -> list[dict]:
    database_connection = connect_to_database()
    if database_connection:
        return json.dumps(retrieve_articles(database_connection, offset, limit))
    else:
        return ("Fetching Unsuccessful", 500) 

@app.route('/fetch_analytic_data')
@cross_origin()
def fetch_analytical_data() -> dict:
    database_connection = connect_to_database()
    if database_connection:
        return json.dumps(retrive_analytics(database_connection))
    else:
        return ("Fetching Unsuccessful", 500) 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)