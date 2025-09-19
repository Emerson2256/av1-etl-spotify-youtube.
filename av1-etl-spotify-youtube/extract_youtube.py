import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd

load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

if not YOUTUBE_API_KEY:
    raise SystemExit('Preencha YOUTUBE_API_KEY no .env')

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Ajuste a consulta conforme seu objetivo (ex: trending, artista, música)
QUERY = 'top music 2025'
MAX_RESULTS = 25

def search_videos(q, max_results=25):
    req = youtube.search().list(q=q, part='snippet', type='video', maxResults=max_results)
    res = req.execute()
    videos = []
    for item in res.get('items', []):
        videos.append({
            'video_id': item['id']['videoId'],
            'title': item['snippet']['title'],
            'channel_title': item['snippet']['channelTitle'],
            'published_at': item['snippet']['publishedAt']
        })
    return pd.DataFrame(videos)

if __name__ == '__main__':
    df = search_videos(QUERY, MAX_RESULTS)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/youtube_videos_raw.csv', index=False)
    print(f'Exported {len(df)} videos to data/youtube_videos_raw.csv')
