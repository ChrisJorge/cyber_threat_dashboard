from flask import Flask
from database import connect_to_database, insert_articles
from web_scraper import scrape_cyber_security_dive, scrape_cyber_security_news, scrape_hacker_news, standardize_time
from classification import extract_cves, extract_tags, remove_punctuation, determine_severity
app = Flask(__name__)

@app.route('/')
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
        
        for url in cyber_security_dive_list:
            scrape_cyber_security_dive(url = url, prefix= url, data = scraped_articles, max_pages = 3, current_page=1)

        for url in cyber_security_news_list:
            scrape_cyber_security_news(url = url, data = scraped_articles, max_pages = 3, current_page=1)

        scrape_hacker_news(url = 'https://thehackernews.com/', data = scraped_articles, max_pages = 3, current_page=1)

        for article in scraped_articles:
            CVES = extract_cves(title = article['title'], text = article['description'])
            article['tags'] = extract_tags(title = article['title'], text = article['description'], matched_tags= article['tags'])
            article['severity'] = determine_severity(tags = article['tags'], cves= CVES)
            for cve in CVES:
                article['tags'].append(cve)
        
        insert_articles(articles=scraped_articles, connection = connect_to_database())

        return ("Scraping Successful", 200)
    return ("Scraping Unsuccessful", 500)
@app.route('/fetch_articles/<offset>/<limit>')
def fetch_articles(offset: int, limit: int) -> list[dict]:
    return f'{offset}, {limit}'
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)