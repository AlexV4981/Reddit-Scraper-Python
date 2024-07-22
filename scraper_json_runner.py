import json

from scraper_db import get_all_from_table 

def convert_to_json(database_file='scraper.db', table_name='redditPosts', output_file='posts.json'):
  """
  Retrieves all posts from the database table and converts them into a JSON file.

  Args:
      database_file (str, optional): The path to the SQLite database file. Defaults to 'scraper.db'.
      table_name (str, optional): The name of the table containing post data. Defaults to 'redditPosts'.
      output_file (str, optional): The name of the output JSON file. Defaults to 'posts.json'.
  """

  # Get all posts from the table
  all_posts = get_all_from_table(database_file, table_name)

  # Check if any posts were retrieved
  if not all_posts:
      print("No posts found in the database.")
      return

  # Convert each post tuple (title, body, url) into a dictionary
  json_data = []
  for title, body, url in all_posts:
      post_dict = {
          "title": title,
          "body": body,
          "url": url
      }
      json_data.append(post_dict)

  # Write the JSON data to a file
  with open(output_file, 'w') as outfile:
      json.dump(json_data, outfile, indent=4)  # Add indentation for readability

  print(f"Posts successfully converted to JSON and saved to '{output_file}'.")

convert_to_json()
