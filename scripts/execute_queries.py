import os
import subprocess
import re

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://rajkaran541:12345@cluster0.fcysb9p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
NEW_QUERIES_FILE = "new_queries.txt"
LOG_FILE = "execution.log"
# DB = "test"

# Set the working directory to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
queries_dir = os.path.join(project_root, "queries")
os.chdir(script_dir)

# Print the current working directory
print(f"Current working directory: {os.getcwd()}")

def execute_queries():
    """Executes all new queries from new_queries.txt."""
    new_queries_file_path = os.path.join(script_dir, NEW_QUERIES_FILE)
    if not os.path.exists(new_queries_file_path):
        print("No new queries found.")
        return False

    with open(new_queries_file_path, "r") as f:
        files = [line.strip() for line in f.readlines()]
        print(files)

    for file in files:
        print(f"Executing {file}...")
        query_file_path = os.path.join(queries_dir, file)
        print(f"Query file path: {query_file_path}")
        if not os.path.exists(query_file_path):
            print(f"File not found: {query_file_path}")
            return False

        with open(query_file_path, "r") as qf:
            query = qf.read().strip().replace("\n", " ")
            print(f"Raw query: {query}")
            match = re.match(r"^([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\.", query)

            if not match:
                print(f"Error: No valid database and collection found in {file}")
                return

            db_name = match.group(1)  # Extracted database name
            print(f"Extracted Database Name: {db_name}")

            # Replace database name with "db" for execution
            query = query.replace(f"{db_name}.", "db.", 1)
            query = query.replace('"', '\\"')
            print(f"Modified query: {query}")
        command = f'mongosh "{MONGO_URI}/{db_name}" --eval "{query}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        with open(LOG_FILE, "a") as log:
            log.write(f"Executing {file}:\n{result.stdout}\n{result.stderr}\n")

        if result.returncode != 0:
            print(f"Execution failed for {file}")
            return False

    print("All queries executed successfully.")
    return True

if __name__ == "__main__":
    if not execute_queries():
        exit(1)  # Fail Jenkins job if execution fails