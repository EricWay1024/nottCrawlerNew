import json
from .all_plans import get_all_plans
from .config import YEAR, PLAN_BRIEF_PATH, DB_PATH
from .database import plan_exists, insert_plan, create_table
from .get_plan import get_plan
import threading
import sqlite3
import concurrent.futures


# Function to insert a plan into the database
def insert_plan_to_db(plan):
    global finished_count

    campus_map = {
        "U": "United Kingdom",
        "M": "Malaysia",
        "C": "China",
    }

    plan_code = plan["code"]
    year = plan["year"]
    campus = plan["campus"]

    # Open connection to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the plan already exists in the database
    if plan_exists(cursor, year, campus_map[campus], plan_code):
        conn.close()
        with counter_lock:
            finished_count += 1
            print(f"Processed {finished_count} out of {total_plans} plans.", end='\r')
        return

    # Get the detailed plan data by calling get_plan
    plan_data = get_plan(plan_code, year, campus)
    insert_plan(cursor, plan_data)
    
    # Commit and close the connection
    conn.commit()
    conn.close()

    # Safely increment the counter and print progress
    with counter_lock:
        finished_count += 1
        print(f"Processed {finished_count} out of {total_plans} plans.", end='\r')


if __name__ == "__main__":
    try:
        # Load the brief data from the JSON file
        plan_objs = json.load(open(PLAN_BRIEF_PATH))
    except FileNotFoundError:
        plan_objs = []
        for campus in ['U', 'C', 'M']:
            plan_objs.extend(get_all_plans(campus, YEAR))
        json.dump(plan_objs, open(PLAN_BRIEF_PATH, 'w'))

    # Counter for finished plans and a lock for thread safety
    finished_count = 0
    total_plans = len(plan_objs)
    counter_lock = threading.Lock()
    
    # Create the table first
    create_table()

    # Use ThreadPoolExecutor to handle the tasks concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit all the plans to the executor for concurrent processing
        futures = [executor.submit(insert_plan_to_db, plan) for plan in plan_objs]
        
        # Ensure all threads finish
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # This will raise any exceptions encountered during execution
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                print(f"Generated an exception: {exc}")