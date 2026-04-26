import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

print("URI:", URI)
print("USER:", USERNAME)
print("PASS:", PASSWORD)

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def run_query(query, params=None):
    with driver.session() as session:
        return list(session.run(query, params))