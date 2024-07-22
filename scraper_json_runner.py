import json
import datetime
from gtts import gTTS
from scraper_db import get_all_from_table 
from scraper_db import scrape_and_save_all_posts
from scraper_db import delete_all_posts

import datetime

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

def convert_json_to_speech(json_file='July_21_posts.json'):
  """
  Converts titles and bodies of posts from a JSON file to separate MP3 files named after the post titles.

  Args:
      json_file (str, optional): The path to the JSON file containing post data. Defaults to 'your_json_file.json'.
  """

  # Load JSON data
  with open(json_file, 'r') as file:
    data = json.load(file)

  # Process each post
  for post in data:
    title = post['title']
    body = post['body']
    url = post['url']

    # Combine title and body for speech
    text_to_speak = f"{title}. {body}. You can view the original post at {url}."  # Mention URL in speech

    # Create gTTS object and save as MP3
    tts = gTTS(text=text_to_speak, lang='en')
    tts.save(f"{title}.mp3")  # Filename based on post title

    # Add URL to MP3 file metadata (limited support, might not work on all players)
    tts.save(f"{title}.mp3")  # Save again with metadata

    print(f"Speech generated and saved as '{title}.mp3'")

 



