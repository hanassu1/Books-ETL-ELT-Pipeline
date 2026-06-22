import os
import pandas as pd
import sqlite3
import requests

CSV_FILE_PATH = "data/Books_Dataset.csv"
DB_PATH = "Books_Dataset.db"
RAW_TABLE = "books_raw"

API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
API_URL = f"https://www.googleapis.com/books/v1/volumes?q=harry+potter&key={API_KEY}"


def extract_csv(file_path):
    return pd.read_csv(file_path)


def extract_api(api_url):
    if not API_KEY:
        print("No API key found. Skipping API extraction.")
        return pd.DataFrame()

    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    data = response.json()

    books = []

    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        books.append({
            "title": info.get("title"),
            "api_publisher": info.get("publisher"),
            "api_published_date": info.get("publishedDate"),
            "api_category": info.get("categories", [None])[0],
            "api_page_count": info.get("pageCount")
        })

    return pd.DataFrame(books)


def load_raw_to_sqlite(df, db_path):
    conn = sqlite3.connect(db_path)

    df.to_sql(
        RAW_TABLE,
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()
    print("Raw data loaded successfully into SQLite.")


def main():
    csv_data = extract_csv(CSV_FILE_PATH)
    api_data = extract_api(API_URL)

    if not api_data.empty:
        raw_data = pd.merge(csv_data, api_data, on="title", how="left")
    else:
        raw_data = csv_data.copy()

    load_raw_to_sqlite(raw_data, DB_PATH)


if __name__ == "__main__":
    main()