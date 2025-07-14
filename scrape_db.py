import sqlite3
from scrape import RedditPostExtractor

DB_FILE = 'scraper.db'

def setup_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS redditPosts (
                title TEXT,
                body TEXT,
                url TEXT
            )
        ''')

def insert_all_posts(scraped):
    with sqlite3.connect(DB_FILE) as conn:
        conn.executemany("INSERT INTO redditPosts VALUES (?,?,?)", scraped.all_post_details)
        conn.commit()

def insert_single_post(scraped, index):
    try:
        post = scraped.all_post_details[index]
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO redditPosts VALUES (?,?,?)", post)
    except IndexError:
        print(f"Invalid index: {index}")
    except sqlite3.Error as e:
        print(f"Insert failed: {e}")

def delete_single_post(title):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM redditPosts WHERE title = ?", (title,))
        conn.commit()
        print(f"Deleted {c.rowcount} post(s) with title: {title}")

def delete_all_posts():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM redditPosts")
        conn.commit()
        print(f"Deleted {c.rowcount} total posts. DB")

def count_posts():
    with sqlite3.connect(DB_FILE) as conn:
        count = conn.execute("SELECT COUNT(*) FROM redditPosts").fetchone()[0]
        print(f"{count} posts in redditPosts.")
        return count

def get_all(table='redditPosts'):
    with sqlite3.connect(DB_FILE) as conn:
        return conn.execute(f"SELECT * FROM {table}").fetchall()

def get_by_index(index, table='redditPosts'):
    with sqlite3.connect(DB_FILE) as conn:
        return conn.execute(f"SELECT * FROM {table} WHERE ROWID = ?", (index,)).fetchone()

def scrape_and_save(subreddit, limit=10, verbose=False):
    setup_db()
    scraper = RedditPostExtractor(subreddit)
    scraper.get_all_post_details(num_posts=limit)
    insert_all_posts(scraper)
    if verbose:
        print(f"Scraped and saved {len(scraper.all_post_details)} posts.")
