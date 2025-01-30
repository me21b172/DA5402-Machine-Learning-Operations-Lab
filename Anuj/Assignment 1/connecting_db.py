import psycopg2
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

conn = hosting_db_locally()
cur = conn.cursor()
# Execute a command: create datacamp_courses table
cur.execute("""CREATE TABLE datacamp_courses(
            course_id SERIAL PRIMARY KEY,
            course_name VARCHAR (50) UNIQUE NOT NULL,
            course_instructor VARCHAR (100) NOT NULL,
            topic VARCHAR (20) NOT NULL);
            """)
# Make the changes to the database persistent
conn.commit()
# Close cursor and communication with the database
cur.close()
conn.close()