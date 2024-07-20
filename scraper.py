import requests
from bs4 import BeautifulSoup

base_url = 'https://www.reddit.com'
subreddit_name = 'TrueOffMyChest'

listings_url = f"{base_url}/r/{subreddit_name}/top/?feedViewType=compactView"

response = requests.get(listings_url)
if response.ok:
    soup = BeautifulSoup(response.content, 'html.parser')
else:
    print(f'Error {response.status_code} while fetching listings URL')


post_links = soup.find_all('a', class_='absolute inset-0')

top_10_links = post_links[:10]

individual_post_urls = []

for link in top_10_links:
    individual_post_urls.append(base_url + link['href'])

print(len(individual_post_urls))



for url in individual_post_urls:
    print(f"{url}")
