from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password123")


class Neo4jGraphApp:

    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def clear_database(self):
        query = "MATCH (n) DETACH DELETE n"
        with self.driver.session() as session:
            session.run(query)
            print("[+] Database cleared successfully.")

    def create_graph(self):
        # Cypher query to create Actors, Directors, Movies, and Relationships
        query = """
        CREATE 
          (keanu:Person {name: 'Keanu Reeves', born: 1964}),
          (carrie:Person {name: 'Carrie-Anne Moss', born: 1967}),
          (laurence:Person {name: 'Laurence Fishburne', born: 1961}),
          (lana:Person {name: 'Lana Wachowski', born: 1965}),
          (matrix:Movie {title: 'The Matrix', released: 1999, tagline: 'Welcome to the Real World'}),
          (matrix2:Movie {title: 'The Matrix Reloaded', released: 2003}),
          (john_wick:Movie {title: 'John Wick', released: 2014}),
          (memento:Movie {title: 'Memento', released: 2000}),

          (keanu)-[:ACTED_IN {role: 'Neo'}]->(matrix),
          (carrie)-[:ACTED_IN {role: 'Trinity'}]->(matrix),
          (laurence)-[:ACTED_IN {role: 'Morpheus'}]->(matrix),
          (lana)-[:DIRECTED]->(matrix),

          (keanu)-[:ACTED_IN {role: 'Neo'}]->(matrix2),
          (carrie)-[:ACTED_IN {role: 'Trinity'}]->(matrix2),
          (lana)-[:DIRECTED]->(matrix2),

          (keanu)-[:ACTED_IN {role: 'John Wick'}]->(john_wick),
          (carrie)-[:ACTED_IN {role: 'Natalie'}]->(memento)
        """
        with self.driver.session() as session:
            session.run(query)
            print(
                "[+] Graph structure created (Nodes: Person, Movie | Edges:"
                " ACTED_IN, DIRECTED)."
            )

    def run_queries(self):
        with self.driver.session() as session:
            print("\n--- Query 1: Find all co-actors of Keanu Reeves ---")
            q1 = """
            MATCH (p:Person {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(coActor:Person)
            RETURN DISTINCT coActor.name AS CoActor, m.title AS Movie
            """
            results = session.run(q1)
            for record in results:
                print(f"Movie: {record['Movie']} | Co-Actor: {record['CoActor']}")

            print("\n--- Query 2: Find Director and Cast of 'The Matrix' ---")
            q2 = """
            MATCH (m:Movie {title: 'The Matrix'})
            OPTIONAL MATCH (director:Person)-[:DIRECTED]->(m)
            OPTIONAL MATCH (actor:Person)-[r:ACTED_IN]->(m)
            RETURN director.name AS Director, actor.name AS Actor, r.role AS Role
            """
            results = session.run(q2)
            for record in results:
                print(
                    f"Director: {record['Director']} | Actor: {record['Actor']}"
                    f" (Role: {record['Role']})"
                )

            print("\n--- Query 3: Recommendation Engine (Related Collaborators) ---")
            q3 = """
            MATCH (p:Person {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(coActor:Person)
            MATCH (coActor)-[:ACTED_IN]->(otherMovie:Movie)
            WHERE NOT (p)-[:ACTED_IN]->(otherMovie)
            RETURN coActor.name AS CoActor, otherMovie.title AS RecommendedMovie
            """
            results = session.run(q3)
            for record in results:
                print(
                    f"Based on collaborator {record['CoActor']}, recommended:"
                    f" {record['RecommendedMovie']}"
                )


if __name__ == "__main__":
    app = Neo4jGraphApp(URI, AUTH)
    app.clear_database()
    app.create_graph()
    app.run_queries()
    app.close()