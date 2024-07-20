import requests
from bs4 import BeautifulSoup
subreddit = 'programming'

url = f'https://www.reddit.com/r/{subreddit}/top/?t=week'

headers = {
    'User-Agent' : 'Protsy_'
}

response = requests.get(url, headers=headers)

if response.ok:
    soup = BeautifulSoup(response.content, 'html.parser')

posts = soup.find_all("article", class_="w-full m-0", limit=20)

for post in posts:
    title_element = post.find('a', class_='title')
    score_element = post.find('span', class_='score')
    if title_element and score_element:
        print("HEY")
        print(f"Title: {title_element.text.strip()}")
        print(f"Score: {score_element.text.strip()}")
       # print('-' * 4)
    else:
        print(f'Error {response.status_code}')



