# #Run the code to orchestrate all the above modules
import psycopg2
from Module1AndModule2Web_scrapping import extract_top_stories
from Module4 import hosting_db_locally,create_tables
from Module5 import is_news_in_database


def insert_data():
    '''Inserting data into database'''
    conn = hosting_db_locally()
    cur = conn.cursor()
    news_data = extract_top_stories()
    for news in news_data:
        if is_news_in_database(cur,news):
            cur.execute("INSERT INTO news_meta_data (news_url,news_title,news_source,date_scraped) VALUES (%s,%s,%s,%s)", (news["link"],news["title"],news["source"],news["timestamp"]))
            cur.execute("INSERT INTO news_image_data (Image,news_title,date_scraped) VALUES (%s,%s,%s)", (psycopg2.Binary(news["image"]),news["title"],news["timestamp"]))
    conn.commit()
    cur.close()
    conn.close()   

# Module 6 : Run the code to orchestrate all the above modules
if __name__ == "__main__":
    create_tables()
    insert_data() 