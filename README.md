
# Neo4j Graph Database & Cypher Query Engine with Python

A graph data platform built on **Neo4j 5.x** and connected via the official Python `neo4j` Bolt driver. This project models interconnected movie production networks, node-edge topologies, and traverses multi-hop entity graphs using Cypher query language.

---

## Architecture & Graph Topology

```text
[ Python Neo4j Driver (Bolt: 7687) ] 
                 │
                 ▼ Cypher AST Execution
     [ Neo4j Graph Database Engine ]
                 │
                 ▼ Web Interface (Port 7474)
      [ Neo4j Browser Visualization ]

Graph Schema
Node Labels:

:Person (Attributes: name, born)
:Movie (Attributes: title, released, tagline)

Relationship Types:

[:ACTED_IN {role: string}]
[:DIRECTED]

Graph Visualization
Core Cypher Queries Implemented
1. Multi-Hop Co-Actor Traversal
Finds all entities collaborating on common movie nodes:
MATCH (p:Person {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(coActor:Person)
RETURN DISTINCT coActor.name AS CoActor, m.title AS Movie;

2. Multi-Relational Pattern Matching
Extracts director entity alongside associated cast members and role metadata:
MATCH (m:Movie {title: 'The Matrix'})
OPTIONAL MATCH (director:Person)-[:DIRECTED]->(m)
OPTIONAL MATCH (actor:Person)-[r:ACTED_IN]->(m)
RETURN director.name AS Director, actor.name AS Actor, r.role AS Role;

3. Graph-Based Recommendation Traversal
Traverses two degrees of separation to identify adjacent project nodes:
MATCH (p:Person {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(coActor:Person)
MATCH (coActor)-[:ACTED_IN]->(otherMovie:Movie)
WHERE NOT (p)-[:ACTED_IN]->(otherMovie)
RETURN coActor.name AS CoActor, otherMovie.title AS RecommendedMovie;

How to Run Locally
1. Start Neo4j via Docker
docker compose up -d
Access UI at http://localhost:7474 (User: neo4j, Password: password123).

2. Execute Driver Script
pip install neo4j
python graph_operations.py
