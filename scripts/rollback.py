import os
import subprocess

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
LOG_FILE = "scripts/execution.log"

def rollback():
    """Rolls back last executed queries if needed."""
    if not os.path.exists(LOG_FILE):
        print("No previous executions to rollback.")
        return False

    with open(LOG_FILE, "r") as log:
        last_executed = log.readlines()[-1]

    rollback_query = last_executed.replace("insertMany", "deleteMany")
    command = f'mongosh "{MONGO_URI}" --eval "{rollback_query}"'
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Rollback successful.")
        return True
    else:
        print("❌ Rollback failed.")
        return False

if __name__ == "__main__":
    rollback()
