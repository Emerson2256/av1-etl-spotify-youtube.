#!/usr/bin/env bash
python extract_spotify.py
python extract_youtube.py
python transform_load.py
echo "ETL completo. Rode: streamlit run app.py"
