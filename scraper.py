import requests
from bs4 import BeautifulSoup


class RedditPostExtractor:
    def __init__(self, subreddit_name):
        self.subreddit_name = subreddit_name
        self.base_url = 'https://www.reddit.com'
        self.after_param = None
        self.all_post_details = []

    def get_listings_url(self):
        listings_url = f"{self.base_url}/r/{self.subreddit_name}/top/?feedViewType=compactView"
        if self.after_param:
            listings_url += f"&after={self.after_param}"
        return listings_url

    def extract_post_details(self, post_url):
        response = requests.get(post_url)
        if response.ok:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Improved selector targeting h1 element with dynamic ID
            title_element = soup.find('h1', id=lambda id_: id_.startswith('post-title-t3_'))

            if title_element:
                # Extract title (handling potential None value)
                title = title_element.text.strip() if title_element else None

                # Existing logic for body element (assuming it's already implemented)
                parent_element = soup.find('div', class_='mb-sm mb-xs px-md xs:px-0')
                if parent_element:
                    body_element = parent_element.find('div', id=lambda id_: id_.startswith('t3_') and id_.endswith('-post-rtjson-content'))
                    text_body = body_element.text.strip() if body_element else None
                else:
                    text_body = "None or Post has no Body"  # Or handle case where parent element is missing

                return title, text_body, post_url
            else:
                # Handle case where title element is missing
                title = "None"
                text_body = "None or Post has no body"  # Or handle differently based on your needs

        else:
            print(f'Error: Could not fetch post content for {post_url}')
            return None, None, None

    def get_all_post_details(self, num_pages=2, print_details=False):
        for page in range(1, num_pages + 1):
            listings_url = self.get_listings_url()
            response = requests.get(listings_url)
            if response.ok:
                soup = BeautifulSoup(response.content, 'html.parser')

                post_links = soup.find_all('a', slot="full-post-link", class_='absolute inset-0')

                for link in post_links:
                    individual_post_url = self.base_url + link['href']

                    # Call the function to extract details from each post URL
                    title, text_body, post_url = self.extract_post_details(individual_post_url)

                    # Append extracted details (or None if error) to the list
                    self.all_post_details.append((title, text_body, post_url))

                last_post = soup.find('a', rel='next')
                if last_post:
                    self.after_param = last_post.get('href').split('=')[-1]
            else:
                print(f'Error {response.status_code} while fetching listings URL')

        if print_details:
            # Print extracted details
            if self.all_post_details:
                for title, body, url in self.all_post_details:
                    print(f"URL: {url}")
                    print(f"Title: {title}")
                    print(f"Body: {body}")
                    print("")  # Add separator between titles
            else:
                print("No posts found or errors occurred while extracting details.")

        return self.all_post_details  # Optionally return the list of extracted details

    #title, body, URL is houw the list is made
    def get_post_by_index(self,index):
            if 0 <= index < len(self.all_post_details):
                return self.all_post_details[index]
            else:
                print(f"Invalid index: {index}. List has {len(self.all_post_details)} elements.")
                return None



if __name__ == "__main__":
    subreddit_name = "TrueOffMyChest"
    reddit_extractor = RedditPostExtractor(subreddit_name)
    reddit_extractor.get_all_post_details(print_details=True)

