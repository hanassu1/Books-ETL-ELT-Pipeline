DROP TABLE IF EXISTS books_transformed;

CREATE TABLE books_transformed AS
SELECT
    "bookID",
    TRIM(title) AS title,
    TRIM(authors) AS authors,

    CAST(average_rating AS FLOAT) AS average_rating,

    CASE 
        WHEN CAST(average_rating AS FLOAT) >= 4 THEN 'High'
        WHEN CAST(average_rating AS FLOAT) >= 3 THEN 'Medium'
        ELSE 'Low'
    END AS rating_category,

    language_code,

    CAST(num_pages AS INTEGER) AS num_pages,

    CASE 
        WHEN CAST(num_pages AS INTEGER) > 300 THEN 'Long'
        ELSE 'Short'
    END AS book_size,

    TRIM(publisher) AS publisher

FROM books_raw

WHERE average_rating IS NOT NULL
  AND CAST(average_rating AS FLOAT) > 0
  AND num_pages IS NOT NULL;