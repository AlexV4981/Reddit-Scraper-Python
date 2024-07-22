import sqlite3
from scraper import RedditPostExtractor

def delete_all_posts(database_file='scraper.db'):
  """Deletes all posts from the specified SQLite database.

  Args:
    database_file (str, optional): The path to the SQLite database file.
      Defaults to 'scraper.db'.

  Returns:
    int: The number of posts deleted, or -1 if an error occurred.
  """

  try:
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    c.execute("DELETE FROM redditPosts") 
    deleted_count = c.rowcount

    # Commit the changes explicitly
    conn.commit()

    print(f"Deleted {deleted_count} posts")
    return deleted_count

  except sqlite3.Error as e:
    print(f"Error deleting posts: {e}")
    return -1 

  finally:
    if conn:
      conn.close()

def insert_all_posts(RedditScrape=RedditPostExtractor):
    """
    Title is index 0
    Body is index 1
    URL is index 2
    """
    conn = sqlite3.connect('scraper.db')
    c = conn.cursor()
    try:
        for post in RedditScrape.all_post_details:
            c.execute("INSERT INTO redditPosts VALUES (?,?,?)",post)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Could not insert posts {e}")
    finally:
        conn.close()

def delete_single_post(Title=str):
    """
    Deletes a post from the redditPosts table based on its title.
    Args:
        title (str): The title of the post to delete.
    Raises:
        sqlite3.Error: If an error occurs during database operations.
    """
    conn = sqlite3.connect('scraper.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM redditPosts WHERE title = ?",(Title))
        conn.commit()
        print(f"Deleted post with title: {Title}")
    except sqlite3.Error as e:
        print(f"Couldnt delete post with the Title:[{Title}]")
    finally:
        conn.close()

def insert_single_post(RedditPost=RedditPostExtractor,Index=int):
    conn = sqlite3.connect('scraper.db')
    c = conn.cursor()

    try:
        Post = RedditPost.all_post_details[Index]
        c.execute("INSERT INTO redditPosts VALUES (?,?,?)",Post)
    except sqlite3.Error as e:
        print(f"Could not insert post {Index}. {e}")
    finally:
        conn.close()

def amount_of_posts():
    """
    Counts the number of posts in the redditPosts table.
    """

    conn = sqlite3.connect('scraper.db')
    c = conn.cursor()

    try:
        c.execute("SELECT COUNT(*) FROM redditPosts")
        count = c.fetchone()[0]  # Assuming count is the only column in the result
        print(f"There are {count} posts in the table.")
    except sqlite3.Error as e:
        print(f"Error counting posts: {e}")
    finally:
        conn.close()

def scrape_and_save_all_posts(Subreddit=str, printAmount=False):
  """
  Scrapes all posts from a specified subreddit and saves them to the database.
  ScrapedPosts must run get_all_post_details to become a list to be used
  printAmount is optional

  Args:
      Subreddit (str): The name of the subreddit to scrape posts from.
      printAmount (bool): Whether or not you want to print the amount of posts scraped.

  Returns:
      None
  """

  # Try creating the table (redditPosts) if it doesn't exist
  try:
      conn = sqlite3.connect('scraper.db')
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS redditPosts (
                  title TEXT,
                  body TEXT,
                  url TEXT
              )''')
      conn.commit()
  except sqlite3.Error as e:
      print(f"Error creating table: {e}")
  finally:
      if conn:
          conn.close()

  # Rest of the original code (without changes)
  # Scrape posts from the specified subreddit
  ScrapedPosts = RedditPostExtractor(Subreddit)
  ScrapedPosts.get_all_post_details(print_details=False)  # Suppress printing details during scraping

  # Insert all scraped posts into the database
  insert_all_posts(ScrapedPosts)

  # Print success message
  print(f"All posts successfully scraped and saved")

  # Print the number of posts in the database (assuming amount_of_posts is a function)
  if printAmount:
      print(amount_of_posts())

def get_all_from_table(database_file='scraper.db', table_name='redditPosts'):
  """
  Retrieves all rows from a table in an SQLite database.

  Args:
    database_file (str, optional): The path to the SQLite database file. Defaults to 'scraper.db'.
    table_name (str, optional): The name of the table to retrieve data from. Defaults to 'redditPosts'.

  Returns:
    list: A list of rows, where each row is a tuple containing the column values.
  """

  conn = sqlite3.connect(database_file)
  c = conn.cursor()

  try:
    # Execute SELECT * query to get all rows
    c.execute(f"SELECT * FROM {table_name}")
    all_rows = c.fetchall()  # Fetch all rows as a list of tuples

    return all_rows

  except sqlite3.Error as e:
    print(f"Error retrieving data: {e}")
    return []  # Return empty list on error

  finally:
    conn.close()

def get_table_by_index(database_file='scraper.db', table_name='redditPosts', index=int):
  """
  Retrieves a specific row from a table based on its index.

  Args:
    database_file (str, optional): The path to the SQLite database file. Defaults to 'scraper.db'.
    table_name (str, optional): The name of the table to retrieve data from. Defaults to 'redditPosts'.
    index (int): The zero-based index of the row to retrieve.

  Returns:
    tuple: A tuple containing the column values of the requested row, or None if the index is invalid.
  """

  conn = sqlite3.connect(database_file)
  c = conn.cursor()

  try:
    # Execute SELECT * query with WHERE clause to filter by index
    c.execute(f"SELECT * FROM {table_name} WHERE ROWID = ?", (index,))
    row = c.fetchone()  # Fetch the single row matching the index

    return row

  except sqlite3.Error as e:
    print(f"Error retrieving data: {e}")
    return None  # Return None on error

  finally:
    conn.close()



