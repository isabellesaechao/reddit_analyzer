#!/bin/bash

# # Prompt the user for input
read -p "Enter the subreddit: " subreddit

python get_reddit_api_data.py "$subreddit"