import base64
from datetime import datetime
import os
import psycopg2
import uvicorn
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Database connection configuration
DB_HOST = os.environ.get("DB_HOST", "localhost")  # Change to "postgres" if using Docker
DB_NAME = os.environ.get("DB_NAME", "rss_feed")
DB_USER = os.environ.get("DB_USER", "rss_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "rss_password")

# Function to connect to PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

@app.get("/news", response_class=HTMLResponse)
async def home(request: Request, date: str = Query(None)):
    """Fetch news articles from the database and display them."""
    if not date:
        return HTMLResponse(content="Please provide a date.", status_code=400)
    
    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return HTMLResponse(content="Invalid date format. Use YYYY-MM-DD.", status_code=400)
    
    conn = get_db_connection()
    if conn is None:
        return HTMLResponse(content="Error connecting to the database.", status_code=500)

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, publication_timestamp, weblink, image, summary 
        FROM articles 
        WHERE DATE(publication_timestamp) = %s
        ORDER BY publication_timestamp DESC;
        """, (selected_date,))
    
    articles = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert articles into dictionary format
    article_list = []
    for article in articles:
        article_dict = {
            "id": article[0],
            "title": article[1],
            "timestamp": article[2],
            "weblink": article[3],
            "summary": article[5],
            "image": None
        }
        if article[4]:  # If image exists
            image_base64 = base64.b64encode(article[4]).decode("utf-8")
            article_dict["image"] = f"data:image/png;base64,{image_base64}"
        
        article_list.append(article_dict)

    return templates.TemplateResponse("website.html", {"request": request, "articles": article_list, "selected_date": selected_date})

@app.get("/", response_class=HTMLResponse)
async def select_date(request: Request):
    """Render the date selection page."""
    return templates.TemplateResponse("date_selection.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
