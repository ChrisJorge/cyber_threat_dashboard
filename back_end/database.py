import os
import psycopg2 as db 
from dotenv import load_dotenv, dotenv_values


def connect_to_database() -> None:
    connection = None
    load_dotenv()
    try:
        params = {
            "host": os.getenv("SERVER"),
            "database": os.getenv("DATABASE"),
            "user": os.getenv("USER"),
            "password": os.getenv("PASSWORD"),
            "port": os.getenv("PORT")
        }
        print(params)
        connection = db.connect(**params)
        return connection
    except db.DatabaseError as error:
        print(f'An error has occurred: {error}')

def create_tables(connection: object) -> None:
    table_scripts =[
    """
        CREATE TABLE IF NOT EXISTS publishers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            severity_level VARCHAR(20) NOT NULL,
            link TEXT UNIQUE NOT NULL,
            publisher_id INT REFERENCES publishers(id),
            published_date TIMESTAMP,
            description TEXT
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS tags (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS article_tags (
            article_id INT REFERENCES articles(id) ON DELETE CASCADE,
            tag_id INT REFERENCES tags(id) ON DELETE CASCADE,
            PRIMARY KEY (article_id, tag_id)
        );
    """ ]
    
    try:
        cursor = connection.cursor()
        for command in table_scripts:
            cursor.execute(command)
            connection.commit()
        cursor.close()
    except db.DatabaseError as error:
        print(f"An error has occurred creating the tables: {error}")

def insert_articles(articles: list, connection: object) -> None:
    try:
        cursor = connection.cursor()
        for article in articles:
            articles_table_check_duplicate_link_query = "SELECT link from articles WHERE link = %s;"
            cursor.execute(articles_table_check_duplicate_link_query, (article['link'],))
            duplicate_check_result = cursor.fetchone()
            if duplicate_check_result == None:
                articles_table_insert_query = "INSERT INTO articles (title, severity_level, link, publisher_id, published_date, description) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
                publisher_table_insert_query = "INSERT INTO publishers (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id;"
                publisher_table_select_query = "SELECT id from publishers WHERE name = %s;"
                tag_table_insert_query = "INSERT INTO tags (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id;"
                tag_table_select_query = "SELECT id from tags WHERE name = %s;"
                article_tags_insert_query = "INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s);"

                cursor.execute(publisher_table_select_query, (article['source'],))
                publisher_check = cursor.fetchone()
                if publisher_check:
                    publisher = publisher_check[0]
                else:
                    cursor.execute(publisher_table_insert_query, (article['source'],))
                    publisher = cursor.fetchone()[0]

                cursor.execute(articles_table_insert_query, (article['title'], article['severity'], article['link'], publisher, article['date'], article['description'],))
                article_id = cursor.fetchone()[0]

                for tag in article['tags']:
                    cursor.execute(tag_table_select_query, (tag,))
                    tag_check = cursor.fetchone()
                    if tag_check:
                        tag_id = tag_check[0]
                    else:
                        cursor.execute(tag_table_insert_query, (tag,))
                        tag_id = cursor.fetchone()[0]
                    cursor.execute(article_tags_insert_query, (article_id, tag_id))
            else:
                continue
        connection.commit()
    except db.DatabaseError as error:
        print(f"An error has occured inserting articles: {error}")
    finally:
        if connection:
            print('Closing connection')
            connection.close()
