import psycopg2
from Module1AndModule2Web_scrapping import extract_top_stories, read_text_file


# Module 4: Create a Python script to store the extracted tuple in a database 
# (one table for storing the image data and the other table for storing the headlines and other meta information)
def create_tables():
    '''Creating Tables'''

    conn = hosting_db_locally()
    cur = conn.cursor()
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
    conn.commit()
    cur.close()
    conn.close()


def hosting_db_locally():
    '''Connecting to database inside the system'''

    DEFAULT_CONFIG = read_text_file()
    try:
        conn = psycopg2.connect(database = DEFAULT_CONFIG["database"], 
                            user = DEFAULT_CONFIG["user"], 
                            host= DEFAULT_CONFIG["host"],
                            password = DEFAULT_CONFIG["password"],
                            port = DEFAULT_CONFIG["port"])
        print("Connected to the database successfully!")
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
