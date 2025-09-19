import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
DB_URL = os.getenv('DATABASE_URL', 'sqlite:///data/db.sqlite')

os.makedirs('data', exist_ok=True)

def load_csv_to_df(path):
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

def prepare_spotify(df):
    if df.empty: return df
    df['duration_sec'] = df['duration_ms'] / 1000.0
    df['popularity'] = df['popularity'].fillna(0).astype(int)
    # keep genre if exists
    cols = ['track_id','name','artists','album','duration_ms','duration_sec','popularity','explicit']
    if 'genre' in df.columns:
        cols.insert(4,'genre')  # insert genre after album
    return df[cols]

def prepare_youtube(df):
    if df.empty: return df
    df['published_at'] = pd.to_datetime(df['published_at'])
    return df[['video_id','title','channel_title','published_at']]

def save_to_db(df, table_name, engine):
    if df.empty:
        print(f'No data for {table_name}, skipping.')
        return
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f'Saved {len(df)} rows to {table_name}')

if __name__ == '__main__':
    spotify_df = load_csv_to_df('data/spotify_tracks_raw.csv')
    youtube_df = load_csv_to_df('data/youtube_videos_raw.csv')

    spotify_prepared = prepare_spotify(spotify_df)
    youtube_prepared = prepare_youtube(youtube_df)

    engine = create_engine(DB_URL, echo=False)

    save_to_db(spotify_prepared, 'spotify_tracks', engine)
    save_to_db(youtube_prepared, 'youtube_videos', engine)

    if not spotify_prepared.empty and not youtube_prepared.empty:
        sample = spotify_prepared.head(10).copy()
        sample['matched_video'] = youtube_prepared['title'].head(10).values
        sample.to_sql('spotify_youtube_sample', engine, if_exists='replace', index=False)
        print('Saved sample cross dataset table spotify_youtube_sample')
