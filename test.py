import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query=Iron Man"

res = requests.get(url).json()

print(res["results"][0]["title"])