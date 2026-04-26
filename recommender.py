from db import run_query

# 🎭 Actor-based recommendation
def recommend_by_actor(actor):
    query = """
    MATCH (a:Actor {name:$name})-[:ACTED_IN]->(m:Movie)
    RETURN m.name AS movie
    """
    result = run_query(query, {"name": actor})
    return [r["movie"] for r in result]


# 🎯 Genre-based recommendation
def recommend_by_genre(genre):
    query = """
    MATCH (m:Movie)-[:BELONGS_TO]->(g:Genre {name:$name})
    RETURN m.name AS movie
    """
    result = run_query(query, {"name": genre})
    return [r["movie"] for r in result]


# 🔥 Similar movie (GRAPH POWER)
def similar_movies(movie):
    query = """
    MATCH (m:Movie {name:$name})<-[:ACTED_IN]-(a:Actor)-[:ACTED_IN]->(rec:Movie)
    WHERE rec.name <> $name
    RETURN DISTINCT rec.name AS recommendation
    """
    result = run_query(query, {"name": movie})
    return [r["recommendation"] for r in result]

def recommend_movies(movie_title):
    query = """
    MATCH (m:Movie {title:$title})<-[:RATED]-(u:User)-[:RATED]->(rec:Movie)
    WHERE rec <> m
    RETURN rec.title AS movie, COUNT(*) AS score
    ORDER BY score DESC
    LIMIT 5
    """
    from db import run_query
    return run_query(query, {"title": movie_title})