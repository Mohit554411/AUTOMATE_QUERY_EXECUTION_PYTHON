import os
import re
import json

NEW_QUERIES_FILE = "new_queries.txt"
# Set the working directory to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
queries_dir = os.path.join(project_root, "queries")
os.chdir(script_dir)

def validate_query_format(query):
    """Check if query follows MongoDB syntax."""
    # Extract the JSON part of the query
    print(f"checking query: {query}")
    json_part = re.search(r"\((.*)\)$", query, re.DOTALL)
    if not json_part:
        return False
    json_str = json_part.group(1).strip()
    print(f"json_part: {json_str}")
    # Validate the JSON part
    try:
        json.loads(json_str)
    except json.JSONDecodeError as e:
        print(e)
        return False

    return True

def validate_queries():
    """Reads new queries and validates them."""
    new_queries_file_path = os.path.join(script_dir, NEW_QUERIES_FILE)
    if not os.path.exists(new_queries_file_path):
        print("No new queries found.")
        return False

    with open(new_queries_file_path, "r") as f:
        files = [line.strip() for line in f.readlines()]

    # queries_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "queries")

    for file in files:
        query_file_path = os.path.join(queries_dir, file)
        if not os.path.exists(query_file_path):
            print(f"❌ File not found: {query_file_path}")
            return False

        with open(query_file_path, "r") as qf:
            query = qf.read().strip()
            if not validate_query_format(query):
                print(f"❌ Invalid query format in {file}")
                return False
    print("✅ All queries are valid.")
    return True

if __name__ == "__main__":
    if not validate_queries():
        exit(1)  # Fail Jenkins job if validation fails