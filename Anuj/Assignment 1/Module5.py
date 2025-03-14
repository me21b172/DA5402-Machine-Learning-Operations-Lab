import psycopg2


# Module 5: Python script to check if a tuple is already present in the DB based on some de-duplication constraint
def is_news_in_database(cur, news):
    '''Check to ensure whether news exists tn the table so as to prevent duplicates in our database'''

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
    result = cur.fetchone()  
    return not result[0]     