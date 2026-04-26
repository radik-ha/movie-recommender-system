import streamlit as st
from recommender import *

st.set_page_config(page_title="Movie Recommender", layout="centered")

st.title("🎬 Movie Knowledge Graph Recommender")

option = st.selectbox(
    "Choose Recommendation Type",
    ["Actor", "Genre", "Similar Movie", "Users Also Liked ⭐"]
)

# 🎭 Actor based
if option == "Actor":
    actor = st.text_input("Enter Actor Name")

    if st.button("Recommend"):
        results = recommend_by_actor(actor)

        if results:
            st.subheader("🎬 Movies:")
            for r in results:
                st.write("👉", r["movie"])
        else:
            st.warning("No results found")

# 🎯 Genre based
elif option == "Genre":
    genre = st.text_input("Enter Genre")

    if st.button("Recommend"):
        results = recommend_by_genre(genre)

        if results:
            st.subheader("🎬 Movies:")
            for r in results:
                st.write("👉", r["movie"])
        else:
            st.warning("No results found")

# 🎬 Similar movies
elif option == "Similar Movie":
    movie = st.text_input("Enter Movie Name")

    if st.button("Recommend"):
        results = similar_movies(movie)

        if results:
            st.subheader("🎬 Similar Movies:")
            for r in results:
                st.write("👉", r["movie"])
        else:
            st.warning("No results found")

# ⭐ NEW: Ratings-based recommender
elif option == "Users Also Liked ⭐":
    movie = st.text_input("Enter Movie Name")

    if st.button("Recommend"):
        results = recommend_movies(movie)

        if results:
            st.subheader("🔥 Recommended:")
            for r in results:
                st.write(f"👉 {r['movie']} (score: {r['score']})")
        else:
            st.warning("No results found")