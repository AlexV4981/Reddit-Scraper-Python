import json
import datetime
import os
import pyttsx3
from scraper_db import get_all_from_table 
from scraper_db import scrape_and_save_all_posts
from scraper_db import delete_all_posts

import datetime

def convert_to_json(database_file='scraper.db', table_name='redditPosts', output_file='posts.json',wipe=True):
    """
    Retrieves all posts from the database table and converts them into a JSON file.
    The output filename is formatted with the current date (Month_Name_Day).

    Args:
        database_file (str, optional): The path to the SQLite database file. Defaults to 'scraper.db'.
        table_name (str, optional): The name of the table containing post data. Defaults to 'redditPosts'.
        output_file (str, optional): The name of the output JSON file (base name). Defaults to 'posts.json'.
    """
        
    # Get all posts from the table
    all_posts = get_all_from_table(database_file, table_name)

    # Check if any posts were retrieved
    if not all_posts:
        print("No posts found in the database.")
        return

    # Get current date in a formatted string (Month_Name_Day)
    today = datetime.date.today()
    formatted_date = today.strftime("%B_%d")  # Use %B for full month name

    # Construct the output filename with date only
    output_file = f"{formatted_date}_{output_file}"

    # Convert posts to JSON (unchanged logic)
    json_data = []
    for title, body, url in all_posts:
        post_dict = {
            "title": title,
            "body": body,
            "url": url
        }
        json_data.append(post_dict)

    # Write the JSON data to the file
    with open(output_file, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)  # Add indentation for readability

    print(f"Posts successfully converted to JSON and saved to '{output_file}'.")
    if wipe:
        print("Wipe is TRUE")
        delete_all_posts()

def scrape_posts_to_db(Subreddit=str):
    scrape_and_save_all_posts(Subreddit)


def sanitize_filename(filename):
    """Sanitize filename by removing or replacing invalid characters."""
    # Replace characters that are not allowed in filenames
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\n', '\r']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def get_unique_filename(file_path):
    base, extension = os.path.splitext(file_path)
    counter = 1

    # Keep checking if the file exists and increment the counter
    while os.path.exists(file_path):
        file_path = f"{base}_{counter}{extension}"
        counter += 1

    return file_path


def convert_json_to_speech(wipe=False):
    """
    Converts titles and bodies of posts from a JSON file to separate MP3 files named after the post titles.
    Prompts the user for the JSON file path.
    """

    # Get JSON file path from user input
    json_file = input("Enter the JSON file for conversion: ")
    json_file += ".json"

    try:
        # Get the current directory where the Python script is located
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Define the folder name
        today = datetime.date.today()
        formatted_date = today.strftime("%B_%d")  # Use %B for full month name
        folder_name = f'{formatted_date}'

        # Create the folder path by joining the current directory and the folder name
        folder_path = os.path.join(current_directory, folder_name)

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f'Folder "{folder_name}" created at {folder_path}')
        else:
            print(f'Folder "{folder_name}" already exists.')

    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")

    # Load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    engine = pyttsx3.init()
    engine.setProperty('rate', 200)  # Adjust speed as needed
    engine.setProperty('volume', 1.0)

    # Process each post
    for post in data:
        title = post['title']
        body = post['body']
        sanitized_title = sanitize_filename(title)
        mp3_file_path = os.path.join(folder_path, f"{sanitized_title}.wav")  # Outputs WAV by default
        mp3_file_path = get_unique_filename(mp3_file_path)
        text_to_speak = f"{title}. {body}."

        # Save speech to file
        engine.save_to_file(text_to_speak, mp3_file_path)
        engine.runAndWait()  # Required to generate the file

        print(f"Speech saved to {mp3_file_path}")

    if wipe:
        delete_all_posts()
