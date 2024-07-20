import requests
from bs4 import BeautifulSoup

response = requests.get(full_post_url)

if response.ok:
  soup = BeautifulSoup(response.content, 'html.parser')
  # Proceed with scraping the individual post using Beautiful Soup
else:
  print(f'Error {response.status_code} while fetching post URL')
