import requests
from bs4 import BeautifulSoup


"""
For this to work the object MUST use get_all_post_details() BEFORE you try and get post information otherwise
it will be empty and it WILL crash

The list of the post is structured title, body, URL

"""

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
                print(title)

                # Existing logic for body element (assuming it's already implemented)
                parent_element = soup.find('div', class_='text-neutral-content', slot='text-body')
                #print(parent_element)

                if parent_element:
                    body_element = parent_element.text.strip()
        
        return title,body_element



    def get_all_post_details(self, num_posts=10, print_details=False):
        seen_posts = set()  # Track seen post URLs to avoid duplicates
        listings_url = self.get_listings_url()  # Get the initial URL
        fetched_posts = 0  # Counter for fetched posts
        
        while fetched_posts < num_posts:
            response = requests.get(listings_url)
            if response.ok:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all post links
                post_links = soup.find_all('a', slot="full-post-link", class_='absolute inset-0')

                for link in post_links:
                    if fetched_posts >= num_posts:
                        break  # Stop if we've reached the required number of posts
                    
                    individual_post_url = self.base_url + link['href']

                    if individual_post_url not in seen_posts:
                        seen_posts.add(individual_post_url)  # Mark as seen
                        title, text_body = self.extract_post_details(individual_post_url)
                        self.all_post_details.append((title, text_body, individual_post_url))
                        fetched_posts += 1  # Increment fetched posts counter

                # Handle pagination using 'after' parameter
                last_post = soup.find('a', rel='next')
                if last_post:
                    next_url = last_post.get('href')
                    listings_url = self.base_url + next_url
                else:
                    break  # No more pages
            else:
                print(f'Error {response.status_code} while fetching listings URL')
                break

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



