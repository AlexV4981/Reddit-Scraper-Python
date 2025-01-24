import argparse

from scraper_db import scrape_and_save_all_posts, delete_all_posts
from scraper_json_runner import convert_json_to_speech, convert_to_json

def main():
  parser = argparse.ArgumentParser(description="Reddit Post Processing Tool")
  parser.add_argument("-s", "--scrape", action="store_true", help="Scrape posts from Reddit")
  parser.add_argument("-j", "--json", action="store_true", help="Convert database to JSON")
  parser.add_argument("-t", "--tts", action="store_true", help="Convert JSON to Text-to-Speech")
  parser.add_argument("-e", "--exit", action="store_true", help="Exit the program")
  parser.add_argument("-r", "--subreddit", help="Subreddit to scrape (for scraping)")
  parser.add_argument("-f", "--file", help="JSON file for conversion (for JSON/TTS)")
  args = parser.parse_args()

  while True:
    print("\nMenu:")
    print("1. Scrape Reddit Posts")
    print("2. Convert to JSON")
    print("3. Convert to Text-to-Speech")
    print("4. Delete All Posts")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == '1':
      # Get subreddit name if needed
      if args.subreddit:
          subreddit = args.subreddit
      else:
          subreddit = input("Enter the subreddit to scrape: ")
      scrape_and_save_all_posts(subreddit)
    elif choice == '2':
      convert_to_json(wipe=True)  # Use default parameters or prompt for them
    elif choice == '3':
      if args.file:
          json_file = args.file
      else:
        convert_json_to_speech()
    elif choice == '4':
      confirmation = input("Are you sure you want to delete all posts? (y/n): ")
      if confirmation.lower() == 'y':
        delete_all_posts()
        print("All posts deleted successfully.")
      else:
        print("Deletion cancelled.")
    elif choice == '5':
      print("Exiting...")
      break
    else:
      print("Invalid choice. Please try again.")

    # Ask to continue
    continue_choice = input("Do you want to continue (y/n)? ")
    if continue_choice.lower() != 'y':
      break

if __name__ == '__main__':
  main()
