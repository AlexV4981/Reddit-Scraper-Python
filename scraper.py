import requests
from bs4 import BeautifulSoup

# Base URL and subreddit name
base_url = 'https://www.reddit.com'
subreddit_name =  input('Must be the EXACT casing of the subreddit name: ')


# Function to extract title and text body from a post URL
def extract_post_details(post_url):
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

            return title, text_body, post_url  # Now returns URL, title, and body
        else:
            # Handle case where title element is missing
            title = "None"
            text_body = "None or Post has no body"  # Or handle differently based on your needs

    else:
        print(f'Error: Could not fetch post content for {post_url}')
        return None, None, None








# Listings URL and pagination
after_param = None
listings_url = f"{base_url}/r/{subreddit_name}/top/?feedViewType=compactView"

all_post_details = []  # List to store extracted titles and bodies

for page in range(1, 3):  # Adjust the range for desired number of pages
    listings_url = f"{base_url}/r/{subreddit_name}/top/?feedViewType=compactView"
    if after_param:
        listings_url += f"&after={after_param}"

    response = requests.get(listings_url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')

        post_links = soup.find_all('a', slot="full-post-link", class_='absolute inset-0')

        for link in post_links:
            individual_post_url = base_url + link['href']

            # Call the function to extract details from each post URL
            title, text_body, post_url = extract_post_details(individual_post_url)

            # Append extracted details (or None if error) to the list
            all_post_details.append((title, text_body, post_url))

        last_post = soup.find('a', rel='next')
        if last_post:
            after_param = last_post.get('href').split('=')[-1]
    else:
        print(f'Error {response.status_code} while fetching listings URL')


# Print extracted details (modify as needed)
if all_post_details:
    for title, body, post_url in all_post_details:
        print(f"--- Post ---")
        if post_url:
            print(f"URL: {post_url}")
        if title:
            print(f"Title: {title}")
        if body:
            print(f"Body:\n{body}")
        print("")  # Add a separator between posts
else:
    print("No posts found or errors occurred while extracting details.")



