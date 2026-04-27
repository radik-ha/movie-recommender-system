import pandas as pd
import requests
from db import run_query
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def clean_title(title):
    return title.split("(")[0].replace(", The", "").strip()


def get_tmdb_id(title):
    try:
        url = f"{BASE_URL}/search/movie"
        params = {
            "api_key": API_KEY,
            "query": clean_title(title)
        }

        res = requests.get(url, params=params, timeout=8)
        data = res.json()

        if data.get("results"):
            return data["results"][0]["id"]

    except Exception as e:
        print("TMDB error:", e)

    return None


def load_movies():
    df = pd.read_csv("data/movies.csv")

    run_query("MATCH (n) DETACH DELETE n")

    print("🚀 Loading movies with TMDB IDs...")

    for _, row in df.iterrows():
        title = row["title"]
        tmdb_id = get_tmdb_id(title)

        run_query("""
        MERGE (m:Movie {id:$id})
        SET m.title = $title,
            m.tmdb_id = $tmdb_id
        """, {
            "id": row["movieId"],
            "title": title,
            "tmdb_id": tmdb_id
        })

    print("✅ Movies loaded with TMDB IDs!")


if __name__ == "__main__":
    load_movies()