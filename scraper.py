import requests
from bs4 import BeautifulSoup


base_url = 'https://www.reddit.com'
subreddit_name = 'TrueOffMyChest'
after_param = None  # Stores the "after" parameter for pagination

all_post_urls = []  # List to store all extracted URLs

for page in range(1, 3):  # Adjust the range for desired number of pages
    listings_url = f"{base_url}/r/{subreddit_name}/top/?feedViewType=compactView"
    if after_param:
        listings_url += f"&after={after_param}"

    response = requests.get(listings_url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Using a specific selector (modify if needed)
        post_links = soup.find_all('a', slot="full-post-link", class_='absolute inset-0')

        for link in post_links:
            individual_post_url = base_url + link['href']
            all_post_urls.append(individual_post_url)

        # Extract "after" parameter from the last post for pagination
        last_post = soup.find('a', rel='next')  # Assuming the "next" link points to the next page
        if last_post:
            after_param = last_post.get('href').split('=')[-1]
    else:
        print(f'Error {response.status_code} while fetching listings URL')

# After iterating through pages, print all extracted URLs
print(len(all_post_urls))
print("Extracted Post URLs:")
for url in all_post_urls:
    print(url)
