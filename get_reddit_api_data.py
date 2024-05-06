"""
following this guide:
https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
https://www.reddit.com/dev/api

and this tutorial video:
https://www.youtube.com/watch?v=FdjVoOf9HN4
"""

import requests
import pandas as pd
import sys
import os

# Reddit API credentials
client_id = 'dOxjnKNuPuC1c4SemG7ykA'
client_secret = 'uYV3uq2tegkTVmcIun4CyXV8soe_0g'

auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

with open('user.txt', 'r') as f:
  user = f.read()

with open('pw.txt', 'r') as f:
  password = f.read()

data = {
  'grant_type' : 'password',
  'username': user,
  'password': password
}

headers = {'User-Agent': 'MyAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).json()


# Use the user input for choosing the subreddit
subreddit = sys.argv[1]
print("Getting results from r/" + subreddit)

url = 'https://oauth.reddit.com/r/' + subreddit + '/hot'
res = requests.get(url,
                 headers=headers, params={'limit': '100'})

df = pd.DataFrame()

for post in res.json()['data']['children']:
  if 'megathread' not in post['data']['title'].lower() and len(post['data']['selftext']) > 0:
    row_to_append = pd.Series({
      'subreddit': post['data']['subreddit'],
      'title': post['data']['title'],
      'selftext': post['data']['selftext'],
      'upvote_ratio': post['data']['upvote_ratio'],
      'entire_post_text': post['data']['title'] + post['data']['selftext']
      })

    df = pd.concat([df, row_to_append.to_frame().T],
      ignore_index=True)

print(df.head(5))

# clear anything existing files in the data folder and add the current information
folder_path = 'data/'
files = os.listdir(folder_path)
for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error removing {file_path}: {e}")

df.to_csv('data/' + subreddit + '_data.csv', index=False)