import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv('DATABASE_URL', 'sqlite:///data/db.sqlite')

st.set_page_config(page_title='ETL Spotify + YouTube', layout='wide')
st.title('ETL — Spotify & YouTube — Dashboard (exemplo melhorado)')

engine = create_engine(DB_URL, echo=False)

@st.cache_data
def load_table(name):
    try:
        return pd.read_sql_table(name, engine)
    except Exception as e:
        return pd.DataFrame()

spotify = load_table('spotify_tracks')
youtube = load_table('youtube_videos')

st.markdown('**Resumo dos dados**')
col1, col2 = st.columns([2,1])

with col1:
    st.subheader('Spotify — tracks')
    if spotify.empty:
        st.info('Nenhum dado Spotify encontrado. Rode extract_spotify.py e transform_load.py primeiro.')
    else:
        st.write(f'Total tracks: {len(spotify)}')
        # filters
        artists = st.multiselect('Filtrar por artista', options=spotify['artists'].unique().tolist(), key='artists_filter')
        genres = spotify['genre'].dropna().unique().tolist() if 'genre' in spotify.columns else []
        genre_choice = None
        if genres:
            genre_choice = st.selectbox('Filtrar por gênero', options=['Todos'] + genres)
        df_filtered = spotify.copy()
        if artists:
            df_filtered = df_filtered[df_filtered['artists'].isin(artists)]
        if genre_choice and genre_choice != 'Todos':
            df_filtered = df_filtered[df_filtered['genre'] == genre_choice]
        st.dataframe(df_filtered.head(50))

        st.subheader('Métricas')
        st.metric('Média de Popularidade', round(df_filtered['popularity'].mean(),2) if not df_filtered.empty else 0)
        st.metric('Duração média (s)', round(df_filtered['duration_sec'].mean(),2) if not df_filtered.empty else 0)

        st.subheader('Gráficos Spotify')
        st.line_chart(df_filtered[['popularity','duration_sec']].head(200))
        # scatter plot
        if not df_filtered.empty:
            st.write('Duração vs Popularidade (scatter)')
            st.altair_chart(
                (st.altair_chart if False else None)  # placeholder to avoid runtime alt import issues in some envs
            )

with col2:
    st.subheader('YouTube — videos')
    if youtube.empty:
        st.info('Nenhum dado YouTube encontrado. Rode extract_youtube.py e transform_load.py primeiro.')
    else:
        st.write(f'Total videos: {len(youtube)}')
        st.dataframe(youtube.head(20))
        st.write('Publicados por canal (top 10)')
        st.bar_chart(youtube['channel_title'].value_counts().head(10))

st.subheader('Sample correlation (spotify_youtube_sample)')
sample = load_table('spotify_youtube_sample')
if sample.empty:
    st.info('Tabela de exemplo não encontrada — execute transform_load.py para criar uma.')
else:
    st.dataframe(sample)
