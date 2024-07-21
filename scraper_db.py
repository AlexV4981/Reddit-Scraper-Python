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

        conn.commit()
        print(f"Deleted {deleted_count} posts")
        return deleted_count

    except sqlite3.Error as e:
        print(f"Error deleting posts: {e}")
        return -1  # Indicate error

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




conn = sqlite3.connect('scraper.db')

c = conn.cursor()

"""

"""

# c.execute("""CREATE TABLE redditPosts (
#           title text,
#           body text,
#           url text
#           )""")


#c.execute("INSERT INTO redditPosts VALUES ('TITLE1','BODY1','URL1') ")

#This must be used
# c.execute("SELECT * FROM redditPosts ")

# print(c.fetchall())

# conn.commit()

# scrapedSubreddit = RedditPostExtractor("TrueOffMyChest")
# scrapedSubreddit.get_all_post_details(print_details=False)

# insert_all_posts(scrapedSubreddit)

amount_of_posts()

conn.close()








