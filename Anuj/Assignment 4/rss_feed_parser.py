import feedparser
import requests
import time
from dateutil import parser
import psycopg2
import os

FEEDS = {
    'Times Of India':'https://timesofindia.indiatimes.com/rssfeeds/1221656.cms',
    'TOI':'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
    'The Hindu': 'https://www.thehindu.com/news/national/?service=rss',
    'Economic Times': 'https://economictimes.indiatimes.com/rssfeedstopstories.cms',
    'India Today' : 'https://www.indiatoday.in/rss/home',
    'NDTV' : 'https://feeds.feedburner.com/ndtvnews-top-stories'
}

DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_NAME = os.environ.get("DB_NAME", "rss_feed")
DB_USER = os.environ.get("DB_USER", "rss_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "rss_password")

def hosting_db():
    '''Connecting to database inside the system'''
    try:
        conn = psycopg2.connect(database = DB_NAME, 
                            user = DB_USER, 
                            host= DB_HOST,
                            password = DB_PASSWORD)
        print("Connected to the database successfully!")
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def download_and_process_image(url):
    '''Loading image from the url'''
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = response.content
        return image
    except Exception as e:
        print(f"Error processing image from {url}: {e}")
        return None
    
def extract_news_data():
    news_data = []
    for source,FEED in FEEDS.items():
        feeds = feedparser.parse(FEED)
        for feed in feeds.entries:
            try:
                # Parse timestamp dynamically
                timestamp = parser.parse(feed["published"]) if "published" in feed else None
            except Exception as e:
                print(f"Error parsing date: {e}")
                timestamp = None
            item = {
                "title": feed.get("title", "").strip(),
                "source": source,
                "timestamp": timestamp,
                "weblink": feed.get("link", ""),
                "image": None,
                "tags": [tag["term"] for tag in feed.get("tags", [])] if "tags" in feed else [],
                "summary": feed.get("summary", ""),
            }
            if "media_content" in feed:
                image_url = feed["media_content"][0]["url"]
                item["image"] = download_and_process_image(image_url)

            elif "links" in feed and len(feed["links"]) > 1:
                image_url = feed["links"][1]["href"]
                item["image"] = download_and_process_image(image_url)

            # Add article to the list given that title and weblink exists
            if item["title"] and item["weblink"]:
                news_data.append(item)

    return news_data

def store_news_data():
    """Store news articles in the database."""
    news_data = extract_news_data()
    conn = hosting_db()
    cursor = conn.cursor()
    for article in news_data:
        cursor.execute(
            """
            INSERT INTO articles (title, publication_timestamp, weblink, image, tags, summary)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (title) DO NOTHING;
            """,
            (article["title"], article["timestamp"], article["weblink"], article["image"], article["tags"], article["summary"])
        )
    print(f"Inserted articles successfully")
    conn.commit()
    cursor.close()
    conn.close()

while(True):
    store_news_data()
    print(len(extract_news_data()))
    time.sleep(60) 