import requests
from bs4 import BeautifulSoup

class RedditPostExtractor:
    def __init__(self, subreddit_name):
        self.subreddit_name = subreddit_name
        self.base_url = 'https://www.reddit.com'
        self.after_param = None
        self.all_post_details = []
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def get_listings_url(self):
        url = f"{self.base_url}/r/{self.subreddit_name}/top/?feedViewType=compactView"
        return f"{url}&after={self.after_param}" if self.after_param else url

    def extract_post_details(self, post_url, print_details=True):
        try:
            response = requests.get(post_url, headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch post: {e}")
            return None, None

        soup = BeautifulSoup(response.content, 'html.parser')

        title_element = soup.find('h1', id=lambda i: i and i.startswith('post-title-t3_'))
        parent_element = soup.find('div', class_='text-neutral-content', slot='text-body')

        title = title_element.text.strip() if title_element else None
        body = parent_element.text.strip() if parent_element else None

        if print_details and title:
            print(title)

        return title, body

    def get_all_post_details(self, num_posts=10, print_details=False):
        seen = set()
        listings_url = self.get_listings_url()
        fetched = 0

        while fetched < num_posts:
            try:
                response = requests.get(listings_url, headers=self.headers)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to load listing page: {e}")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            post_links = soup.find_all('a', slot="full-post-link", class_='absolute inset-0')

            for link in post_links:
                if fetched >= num_posts:
                    break

                url = self.base_url + link['href']
                if url in seen:
                    continue

                seen.add(url)
                title, body = self.extract_post_details(url)
                if title or body:
                    self.all_post_details.append((title, body, url))
                    fetched += 1

            next_button = soup.find('a', rel='next')
            if next_button:
                listings_url = self.base_url + next_button.get('href')
            else:
                break

        if print_details:
            for title, body, url in self.all_post_details:
                print(f"\nURL: {url}\nTitle: {title}\nBody: {body}\n")

        return self.all_post_details

    def get_post_by_index(self, index):
        try:
            return self.all_post_details[index]
        except IndexError:
            print(f"Invalid index: {index}. Max: {len(self.all_post_details) - 1}")
            return None
