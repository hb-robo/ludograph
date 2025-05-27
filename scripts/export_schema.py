"""
Exports the schema of a Neo4j database—including nodes, relationships, 
constraints, and indexes to a YAML file using Cypher schema procedures.
"""

import os
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError, CypherSyntaxError
import yaml

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")


def run_query(tx, query):
    """
    Executes a Cypher query within a Neo4j transaction and returns the results 
    as a list of dictionaries.
    """
    result = tx.run(query)
    return [record.data() for record in result]


if __name__ == '__main__':
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    try:
        with driver.session() as session:
            nodes = session.execute_read(run_query, """
                CALL db.schema.nodeTypeProperties()
                YIELD nodeLabels, propertyName, propertyTypes
                RETURN nodeLabels, propertyName, propertyTypes
                ORDER BY nodeLabels, propertyName
            """)
            relationships = session.execute_read(run_query, """
                CALL db.schema.relTypeProperties()
                YIELD relType, propertyName, propertyTypes
                RETURN relType, propertyName, propertyTypes
                ORDER BY relType, propertyName
            """)
            constraints = session.execute_read(
                run_query, "CALL db.constraints()")
            indexes = session.execute_read(run_query, "CALL db.indexes()")

        OUTPUT_DIR = "../schema"
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        with open(os.path.join(OUTPUT_DIR, "lg_nodes.yaml"),
                  "w", encoding='utf-8') as f:
            yaml.dump(nodes, f, sort_keys=False, default_flow_style=False)
        with open(os.path.join(OUTPUT_DIR, "lg_relationships.yaml"),
                  "w", encoding='utf-8') as f:
            yaml.dump(relationships, f, sort_keys=False,
                      default_flow_style=False)
        with open(os.path.join(OUTPUT_DIR, "lg_constraints.yaml"),
                  "w", encoding='utf-8') as f:
            yaml.dump(constraints, f, sort_keys=False,
                      default_flow_style=False)
        with open(os.path.join(OUTPUT_DIR, "lg_indexes.yaml"),
                  "w", encoding='utf-8') as f:
            yaml.dump(indexes, f, sort_keys=False, default_flow_style=False)

        print("Schema exported to separate YAML files in ../schema/")

    except ServiceUnavailable:
        print("Could not connect to the Neo4j database. Check your URI and network.")
    except AuthError:
        print("Authentication to Neo4j failed. Check your username and password.")
    except CypherSyntaxError as e:
        print(f"Cypher syntax error: {e}")
    except (OSError, IOError) as e:
        print(f"File write error: {e}")
    except yaml.YAMLError as e:
        print(f"YAML serialization error: {e}")

    finally:
        driver.close()
