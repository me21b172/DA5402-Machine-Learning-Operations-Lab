CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    publication_timestamp TIMESTAMP NOT NULL UNIQUE,
    weblink TEXT NOT NULL,
    image BYTEA, -- Storing image as binary (optional)
    tags TEXT[], -- Array of text tags
    summary TEXT,
    CONSTRAINT unique_publication UNIQUE (publication_timestamp, weblink)
);
