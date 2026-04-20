import psycopg2
import requests
import re
import time

DB_SETTINGS = {
    "dbname": "gutenberg_search",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

BOOK_IDS = [1342, 11, 84, 1661, 98, 76, 1952, 174]

START_MARKER_RE = re.compile(r"\*\*\*\s*START OF (THIS|THE) PROJECT GUTENBERG EBOOK.*\*\*\*", re.IGNORECASE)
END_MARKER_RE = re.compile(r"\*\*\*\s*END OF (THIS|THE) PROJECT GUTENBERG EBOOK.*\*\*\*", re.IGNORECASE)

TITLE_RE = re.compile(r"Title:\s*(?P<title>.+)", re.IGNORECASE)
AUTHOR_RE = re.compile(r"Author:\s*(?P<author>.+)", re.IGNORECASE)
LANG_RE = re.compile(r"Language:\s*(?P<lang>.+)", re.IGNORECASE)

def fetch_and_parse_book(gutenberg_id):
    url = f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}-0.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании книги ID {gutenberg_id}: {e}")
        return None

    title_match = TITLE_RE.search(text)
    author_match = AUTHOR_RE.search(text)
    lang_match = LANG_RE.search(text)

    title = title_match.group('title').strip() if title_match else "Unknown Title"
    author = author_match.group('author').strip() if author_match else "Unknown Author"
    language = lang_match.group('lang').strip().lower() if lang_match else "english"
    
    start_match = START_MARKER_RE.search(text)
    end_match = END_MARKER_RE.search(text)

    if start_match and end_match:
        content = text[start_match.end():end_match.start()].strip()
    else:
        content = text

    print(f"  > Найдена книга: '{title}' от '{author}'")
    
    return {
        "gutenberg_id": gutenberg_id,
        "title": title,
        "author": author,
        "language_code": language[:10],
        "content": content
    }

def main():
    conn = None
    try:
        print("Подключение к базе данных...")
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()
        print("Подключение успешно.")

        for book_id in BOOK_IDS:
            print(f"\nОбработка книги с ID: {book_id}...")
            book_data = fetch_and_parse_book(book_id)
            
            if book_data:
                sql = """
                INSERT INTO books (gutenberg_id, title, author, language_code, content)
                VALUES (%(gutenberg_id)s, %(title)s, %(author)s, %(language_code)s, %(content)s)
                ON CONFLICT (gutenberg_id) DO NOTHING;
                """
                cursor.execute(sql, book_data)
                print(f"  > Книга ID {book_id} добавлена в базу данных.")
            
            time.sleep(1) 

        conn.commit()
        cursor.close()
        print("\nВсе книги успешно загружены.")

    except psycopg2.Error as e:
        print(f"Ошибка при работе с PostgreSQL: {e}")
    finally:
        if conn:
            conn.close()
            print("Соединение с базой данных закрыто.")

if __name__ == "__main__":
    main()