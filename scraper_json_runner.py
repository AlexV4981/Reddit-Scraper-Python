import json
import datetime
import os
from gtts import gTTS
from scraper_db import get_all_from_table 
from scraper_db import scrape_and_save_all_posts
from scraper_db import delete_all_posts

import datetime

def convert_to_json(database_file='scraper.db', table_name='redditPosts', output_file='posts.json'):
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


def convert_json_to_speech():
    """
    Converts titles and bodies of posts from a JSON file to separate MP3 files named after the post titles.
    Prompts the user for the JSON file path.
    """

    # Get JSON file path from user input
    json_file = input("Enter the JSON file for conversion: ")

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

    # Process each post
    for post in data:
        title = post['title']
        body = post['body']
        url = post['url']

        # Sanitize the title to make it a valid filename
        sanitized_title = sanitize_filename(title)

        # Combine title and body for speech
        text_to_speak = f"{title}. {body}. You can view the original post at {url}."

        # Create the MP3 file path inside the folder
        mp3_file_path = os.path.join(folder_path, f"{sanitized_title}.mp3")
        mp3_file_path = get_unique_filename(mp3_file_path)

        # Create gTTS object and save as MP3 inside the created folder
        tts = gTTS(text=text_to_speak, lang='en', slow=False)  # Normal speed
        tts.save(mp3_file_path)  # Save the file in the created folder

        print(f"Speech generated and saved as '{mp3_file_path}'")

convert_json_to_speech()


