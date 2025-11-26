import requests
from bs4 import BeautifulSoup as scraper
from classification import remove_punctuation

def standardize_time(date: str) -> str:
    date = remove_punctuation(date).split(' ')
    
    months = {
        'January': 1,
        'Jan': 1,
        'February': 2,
        "Feb": 2,
        "March": 3,
        "Mar": 3,
        "April": 4,
        "Apr": 4,
        "May": 5,
        "June": 6,
        "Jun": 6,
        "July": 7,
        "Jul": 7,
        "August": 8,
        "Aug": 8,
        "September": 9,
        "Sep": 9,
        "October": 10,
        "Oct": 10,
        "November": 11,
        "Nov": 11,
        "December": 12,
        "Dec": 12
        }
    
    month = date[0]
    if month in months:
        date[0] = str(months[month])
    else:
        return None
    
    if len(date) != 3:
        return None
    
    formatted_date = f'{date[2]}-{date[0]}-{date[1]}'
    return formatted_date

def scrape_hacker_news(url: str, data: list, max_pages: int = 1, current_page: int = 1) -> list:
    """Scrapes news from the hacker news website and returns a list of scraped articles with each element as a dictionary"""
    extracted_article_data = data
    request_information = requests.get(url)
    content = scraper(request_information.content, features = 'html.parser')
    articles = content.select("div.body-post")

    for index in range(len(articles)):
        article = articles[index]
        link  = article.select_one("a")
        title = article.select_one("h2.home-title")
        date  = article.select_one("span.h-datetime")
        tags  = article.select_one("span.h-tags")
        desc  = article.select_one("div.home-desc")

        article_link = link["href"]
        article_title = title.get_text(strip=True)
        article_description = desc.get_text(strip=True)
        
        article_publish_date = standardize_time(date.get_text(strip=True).lstrip(": "))

        article_tags = tags.get_text(" ", strip=True).split('/')

        if not(article_link) or not(article_title) or not(article_publish_date) or not(article_description):
            continue

        data = {
            "link": article_link,
            "title": article_title,
            "date": article_publish_date,
            "tags": article_tags,
            "description": article_description,
            "source": "The Hacker News"
        }

        extracted_article_data.append(data)
    if max_pages != current_page:
        next_page = content.select_one('a.blog-pager-older-link-mobile')
        if next_page['href']:
            print(f'Going to scrape {next_page['href']}')
            scrape_hacker_news(next_page['href'], extracted_article_data, max_pages, current_page + 1)
    return extracted_article_data

def scrape_cyber_security_news(url: str, data: list, max_pages: int = 1, current_page: int = 1) -> list:

    extracted_article_data = data
    headers = {'User-Agent': 'MyPythonApp/1.0'}
    request_information = requests.get(url,headers=headers)
    content = scraper(request_information.content, features = 'html.parser')
    articles = content.select("div.td_module_11")

    for index in range(len(articles)):
        article = articles[index]
        link = article.select_one('a')
        article_link = link['href']
        article_title = link['title']
        article_publish_date = standardize_time(article.select_one('time').get_text(strip=True))
        article_description = article.select_one('div.td-excerpt').get_text(strip=True)

        if not(article_link) or not(article_title) or not(article_publish_date) or not(article_description):
            continue 

        data = {
            "link": article_link,
            "title": article_title,
            "date": article_publish_date,
            "tags": [],
            "description": article_description,
            "source": "Cyber Security News"
        }

        extracted_article_data.append(data)
    if max_pages != current_page:
        next_page = content.select_one('a.page')
        if next_page['href']:
            print(f'Going to scrape {next_page['href']}')
            scrape_cyber_security_news(next_page['href'], extracted_article_data, max_pages, current_page + 1)
    return extracted_article_data

# Cyber Security Dive
def scrape_cyber_security_dive(url: str, prefix: str, data: list, max_pages: int = 1, current_page: int = 1) -> list:
    extracted_article_data = data
    request_information = requests.get(url)
    content = scraper(request_information.content, features = 'html.parser')
    articles = content.select("li.feed__item")
    for index in range(len(articles)):
        article = articles[index]
        link = article.select_one('a')
        article_title = article.select_one('h3.feed__title')
        if article_title:
            article_title = article_title.get_text(strip=True)
        else:
            continue

        article_description = article.select_one('p.feed__description').get_text(strip = True)
        article_publish_date_list = article.find_all('span')

        if len(article_publish_date_list) != 2:
            continue
        
        article_publish_date = standardize_time(article_publish_date_list[1].get_text(strip = True).replace("Updated","").strip())
        article_link = f'{url}{link['href']}'

        if not(article_title) or not(article_description) or not(article_publish_date) or not(article_link):
            continue 
            
        data = {
            "link": article_link,
            "title": article_title,
            "date": article_publish_date,
            "tags": [],
            "description": article_description,
            "source": "Cyber Security Dive"
        }
        extracted_article_data.append(data)
    
    if max_pages != current_page:
        print(f'going to scrape {prefix}?page={current_page + 1}')
        scrape_cyber_security_dive(f'{prefix}?page={current_page + 1}', prefix, extracted_article_data, max_pages, current_page + 1)
    return extracted_article_data
