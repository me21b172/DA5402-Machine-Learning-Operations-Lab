import psycopg2
from web_scrapping import extract_top_stories
def hosting_db_locally():
    try:
        conn = psycopg2.connect(database = "image_captioning", 
                            user = "postgres", 
                            host= 'localhost',
                            password = "AnujS@003",
                            port = 5432)
        print("Connected to the database successfully!")
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def create_tables():
    conn = hosting_db_locally()
    cur = conn.cursor()
    # Execute a command: create datacamp_courses table
    # print(table_check)
    cur.execute("""CREATE TABLE IF NOT EXISTS news_image_data (
                    image_id SERIAL PRIMARY KEY,
                    news_title TEXT NOT NULL,
                    Image TEXT NOT NULL ,
                    date_scraped TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );
                """)
    cur.execute("""CREATE TABLE IF NOT EXISTS news_meta_data (
                    news_id SERIAL PRIMARY KEY,
                    news_url TEXT NOT NULL ,
                    news_title TEXT NOT NULL,
                    news_source TEXT NOT NULL,
                    date_scraped TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );
                """)
        # Make the changes to the database persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()
def is_news_in_database(cur, news):
    cur.execute(
        """
        SELECT EXISTS(
            SELECT 1
            FROM news_meta_data
            WHERE news_url = %s
            AND news_title = %s
        )
        """,
        (news["link"], news["title"])
    )
    result = cur.fetchone()  # fetch the single row returned
    return not result[0]         # return the boolean value

def insert_data():
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
create_tables()
insert_data()