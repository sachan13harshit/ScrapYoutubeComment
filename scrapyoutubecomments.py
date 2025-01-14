# -*- coding: utf-8 -*-
"""ScrapYoutubeComments.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CB7U3AgqaZmhPOtKdKQZhil4Rq6N9jyU
"""

import googleapiclient.discovery
import sqlite3


conn = sqlite3.connect('comments.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY,
        video_id TEXT,
        comment_text TEXT
    )
''')

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyBhwsMPfypj-5beybqIVk5MAdn3G3YrJ1Q"

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

video_id = "gd7BXuUQ91w"
max_results = 1000
next_page_token = None
comments = []

while len(comments) < max_results:
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=min(100, max_results - len(comments)),
        pageToken=next_page_token
    )
    response = request.execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comment_text = comment['textDisplay']
        comments.append(comment_text)


        cursor.execute('''
            INSERT INTO comments (video_id, comment_text)
            VALUES (?, ?)
        ''', (video_id, comment_text))

    next_page_token = response.get('nextPageToken')

    if not next_page_token:
        break


conn.commit()
conn.close()

formatted_comments = []
for i, comment in enumerate(comments):
    formatted_comments.append(f"{i + 1}. {comment}\n")


print("\n".join(formatted_comments))