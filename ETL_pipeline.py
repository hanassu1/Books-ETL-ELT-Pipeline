import pandas as pd
import sqlite3
import requests
import os

CSV_FILE_PATH = "data/Books_Dataset.csv"
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
API_URL = f"https://www.googleapis.com/books/v1/volumes?q=harry+potter&key={API_KEY}"
DB_PATH = "database/Books_Dataset.db"

table_name = "Books"


# ETL - Extract from CSV
def extract_csv(file_path):
    try:
        print("Reading CSV file")
        return pd.read_csv(file_path)

    except Exception as e:
        print(f"Could not read CSV file: {e}")
        print("Using default Books data")

        default_data = {
            "bookID": [1, 2, 4, 5, 8],
            "title": [
                "Harry Potter and the Half-Blood Prince",
                "Harry Potter and the Order of the Phoenix",
                "Harry Potter and the Chamber of Secrets",
                "Harry Potter and the Prisoner of Azkaban",
                "Harry Potter Boxed Set 1-5"
            ],
            "authors": [
                "J.K. Rowling",
                "J.K. Rowling",
                "J.K. Rowling",
                "J.K. Rowling",
                "J.K. Rowling"
            ],
            "average_rating": [4.57, 4.49, 4.42, 4.56, None],
            "ratings_count": [2095690, 2153167, 6333, 2339585, 41428],
            "language_code": ["eng", "eng", "eng", "eng", "eng"],
            "num_pages": [652, 870, 251, 435, 2690],
            "publisher": ["Scholastic", "Scholastic", "Scholastic", "Scholastic", "Scholastic"]
        }

        return pd.DataFrame(default_data)


# ETL - Extract from API
def extract_api(api_url):
    try:
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

    except Exception as e:
        print(f"Warning: Could not fetch data from API - {e}")
        return pd.DataFrame()


# ETL - Transform
def merge_and_clean_data(csv_data, api_data):
    csv_data.columns = csv_data.columns.str.strip()

    if api_data is None or api_data.empty:
        print("Using CSV data only")
        merged_data = csv_data.copy()
    else:
        merged_data = pd.merge(
            csv_data,
            api_data,
            on="title",
            how="left"
        )

    merged_data = merged_data.drop_duplicates(subset=["title"])

    text_cols = ["title", "authors", "publisher"]

    for col in text_cols:
        if col in merged_data.columns:
            merged_data[col] = merged_data[col].astype(str).str.strip()

    if "language_code" in merged_data.columns:
        merged_data["language_code"] = merged_data["language_code"].astype(str).str[:2]

    if "authors" in merged_data.columns:
        merged_data["authors"] = merged_data["authors"].str.replace("/", ",", regex=False)

    merged_data["average_rating"] = pd.to_numeric(
        merged_data["average_rating"],
        errors="coerce"
    )

    merged_data = merged_data[merged_data["average_rating"] > 0]

    merged_data["num_pages"] = pd.to_numeric(
        merged_data["num_pages"],
        errors="coerce"
    ).fillna(0)

    merged_data["rating_category"] = merged_data["average_rating"].apply(
        lambda x: "High" if x >= 4 else "Medium" if x >= 3 else "Low"
    )

    merged_data["book_size"] = merged_data["num_pages"].apply(
        lambda x: "Long" if x > 300 else "Short"
    )

    required_columns = [
        "bookID",
        "title",
        "authors",
        "average_rating",
        "rating_category",
        "language_code",
        "num_pages",
        "book_size",
        "publisher",
        "api_publisher",
        "api_published_date",
        "api_category",
        "api_page_count"
    ]

    merged_data = merged_data[required_columns]

    print("Data Successfully Merged, Cleaned, and Transformed")

    return merged_data


# ETL - Validation
def validate_data(merged_data):
    print("\nValidation Results:")

    print("\nNull values:")
    print(merged_data.isnull().sum())

    print("\nDuplicate rows:")
    print(merged_data.duplicated().sum())

    print("\nData types:")
    print(merged_data.dtypes)

    print("\nAverage rating by category:")
    print(merged_data.groupby("rating_category")["average_rating"].mean())


# ETL - Load to SQLite
def load_to_sqlite(merged_data, db_path):
    try:
        conn = sqlite3.connect(db_path)

        merged_data.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        conn.close()

        print("Merged Data Loaded Successfully into SQLite")

    except Exception as e:
        print(f"Error loading data to SQLite: {e}")


def main():
    print("Starting ETL process..")

    csv_data = extract_csv(CSV_FILE_PATH)
    api_data = extract_api(API_URL)

    print("\nAPI Data Preview:")
    print(api_data.head())

    merged_cleaned_data = merge_and_clean_data(csv_data, api_data)

    print("\nFinal Data Preview:")
    print(merged_cleaned_data.head())

    validate_data(merged_cleaned_data)

    load_to_sqlite(merged_cleaned_data, DB_PATH)

    print("\nETL Process Completed!")


if __name__ == "__main__":
    main()

