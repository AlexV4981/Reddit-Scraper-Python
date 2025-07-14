import os
import json
import datetime
import pyttsx3
import scrape_db

DB_FILE = 'scraper.db'
TABLE_NAME = 'redditPosts'


def scrape_posts(subreddit):
    scrape_db.scrape_and_save_all_posts(subreddit)


def convert_to_json(output_file='posts.json', wipe=True):
    folder = (f"Json Files")
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder)
    os.makedirs(folder_path, exist_ok=True)
    posts = scrape_db.get_all()
    if not posts:
        print("No posts found.")
        return

    date_str = datetime.date.today().strftime("%B_%d")
    output_file = f"{date_str}_{output_file}"
    output_path = os.path.join(folder_path, output_file)

    data = [{"title": t, "body": b, "url": u} for t, b, u in posts]
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Saved {len(data)} posts to '{output_file}'\n{folder_path}")
    if wipe:
        scrape_db.delete_all_posts()


def sanitize_filename(name):
    for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\n', '\r']:
        name = name.replace(char, '_')
    return name


def get_unique_path(path):
    base, ext = os.path.splitext(path)
    count = 1
    while os.path.exists(path):
        path = f"{base}_{count}{ext}"
        count += 1
    return path


def convert_json_to_speech(wipe=False):
    json_folder = f"{os.path.join(os.path.dirname(os.path.abspath(__file__)))}\\Json Files"
    json_file = input("Enter the JSON filename (without .json): ") + ".json"
    json_path = os.path.join(json_folder,json_file)
    if not os.path.exists(json_path):
        print(json_path)
        print("File not found.")
        return

    folder = f"{datetime.date.today().strftime('%B_%d')} TTS"
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder)
    os.makedirs(folder_path, exist_ok=True)

    with open(json_path, 'r') as f:
        posts = json.load(f)

    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 1.0)

    for post in posts:
        title = sanitize_filename(post['title'])
        body = post['body']
        speech = f"{post['title']}. {body}."
        filepath = get_unique_path(os.path.join(folder_path, f"{title}.wav"))
        engine.save_to_file(speech, filepath)
        print(f"Queued: {filepath}")

    engine.runAndWait()

    if wipe:
        scrape_db.delete_all_posts()
