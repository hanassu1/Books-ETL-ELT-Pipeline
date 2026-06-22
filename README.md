# Books ETL and ELT Pipeline

A Data Engineering project that demonstrates both ETL and ELT approaches using a books dataset, Google Books API, Python, SQL, and SQLite.

## Project Overview

This project compares two data pipeline approaches:

```text
ETL: Extract → Transform → Load
ELT: Extract → Load → Transform
```

The ETL pipeline cleans and transforms the data in Python before loading it into SQLite.  
The ELT pipeline loads raw data into SQLite first, then transforms it using SQL.

## Project Structure

```text
Books-ETL-ELT-Pipeline/
├── ETL_pipeline.py
├── load_raw_data.py
├── transform_books.sql
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── Books_Dataset.csv
```

## Data Sources

- CSV file: `Books_Dataset.csv`
- API source: Google Books API

## ETL Pipeline

File:

```text
ETL_pipeline.py
```

The ETL pipeline performs the following steps:

1. Extract data from the CSV file.
2. Extract additional book information from Google Books API.
3. Merge CSV and API data.
4. Clean and transform the data using Python.
5. Validate missing values, duplicates, data types, and rating categories.
6. Load the final transformed data into SQLite.

Main transformations include:

- Removing duplicate books by title
- Trimming text columns
- Cleaning author names
- Standardizing language codes
- Converting ratings and page numbers to numeric types
- Creating `rating_category`
- Creating `book_size`

## ELT Pipeline

Files:

```text
load_raw_data.py
transform_books.sql
```

The ELT pipeline performs the following steps:

1. Extract data from the CSV file.
2. Extract additional data from Google Books API.
3. Load raw data into SQLite table `books_raw`.
4. Transform and clean the raw data using SQL.
5. Create the final transformed table `books_transformed`.

Main SQL transformations include:

- Trimming text columns
- Casting rating and page number columns
- Removing invalid ratings
- Removing rows with missing page numbers
- Creating `rating_category`
- Creating `book_size`

## Final Tables

| Pipeline | Output Table |
|---|---|
| ETL | `Books` |
| ELT | `books_transformed` |

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the ETL pipeline:

```bash
python ETL_pipeline.py
```

Run the ELT loading script:

```bash
python load_raw_data.py
```

Then run the SQL transformation:

```bash
sqlite3 Books_Dataset.db < transform_books.sql
```

## Technologies Used

- Python
- Pandas
- Requests
- SQLite
- SQL
- Google Books API

## Environment Variables

Do not upload your API key directly to GitHub.  
Use an environment variable instead:

```text
GOOGLE_BOOKS_API_KEY=your_api_key_here
```

## Important Notes

- The dataset should be placed inside the `data/` folder.
- The project should not upload `.env` files or generated database files.
- If the API key is not provided, the project can still run using the CSV data.

## Project Type

Data Engineering  
ETL Pipeline  
ELT Pipeline  
SQLite Transformation Project

## Author

Hana Alsalman, Maha Alzahrani, Lama Alanzi, Taif Alfaifi, Fajr Alhajry
Data Science and Analytics Students  
Princess Nourah bint Abdulrahman University