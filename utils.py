#AVOID CIRCULAR IMPORTS PLEASE

from scraper_db import return_archive_body_url
from scraper import RedditPostExtractor  # Ensure this is correctly imported

def check_for_updates():
    set_of_tupled_posts = return_archive_body_url()

    extractor = RedditPostExtractor()  # Create an instance if it's not a static method

    for post in set_of_tupled_posts:
        body, link = post

        if extractor.extract_post_details(link,False) == body:  # Use instance to call method
            print(link)





check_for_updates()