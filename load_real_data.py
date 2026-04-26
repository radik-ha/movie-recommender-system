import pandas as pd
from db import run_query

def load_movies():
    df = pd.read_csv("data/movies.csv")

    # Clear DB
    run_query("MATCH (n) DETACH DELETE n")

    # Movies
    movies = df.to_dict("records")

    run_query("""
    UNWIND $movies AS row
    MERGE (m:Movie {id: row.movieId})
    SET m.title = row.title
    """, {"movies": movies})

    # Genres
    genre_data = []
    for _, row in df.iterrows():
        genres = row["genres"].split("|")
        for g in genres:
            genre_data.append({
                "movieId": row["movieId"],
                "genre": g
            })

    run_query("""
    UNWIND $data AS row
    MATCH (m:Movie {id: row.movieId})
    MERGE (g:Genre {name: row.genre})
    MERGE (m)-[:BELONGS_TO]->(g)
    """, {"data": genre_data})

    print("✅ Movies loaded!")


def load_ratings():
    import pandas as pd
    from db import run_query

    df = pd.read_csv("data/ratings.csv")

    batch_size = 5000

    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size].to_dict("records")

        run_query("""
        UNWIND $ratings AS row
        MERGE (u:User {id: row.userId})
        MERGE (m:Movie {id: row.movieId})
        MERGE (u)-[:RATED {rating: row.rating}]->(m)
        """, {"ratings": batch})

        print(f"Loaded {i + batch_size} / {len(df)}")

    print("✅ Ratings loaded successfully!")

if __name__ == "__main__":
    load_movies()
    load_ratings()