import sqlite3
import os

# File paths for the databases
modules_db = 'modules.db'
plans_db = 'plans.db'
combined_db = 'data.db'

# Check if the combined database already exists and delete it to start fresh
if os.path.exists(combined_db):
    os.remove(combined_db)

# Connect to the new combined database
conn_combined = sqlite3.connect(combined_db)
cursor_combined = conn_combined.cursor()

# Attach the modules.db and plans.db to the combined.db session
cursor_combined.execute("ATTACH DATABASE ? AS modules_db", (modules_db,))
cursor_combined.execute("ATTACH DATABASE ? AS plans_db", (plans_db,))

# Step 1: Create the modules table in combined.db by copying from modules.db
cursor_combined.execute('''
    CREATE TABLE IF NOT EXISTS course AS SELECT * FROM modules_db.modules;
''')

# Step 2: Create the plans table in combined.db by copying from plans.db
cursor_combined.execute('''
    CREATE TABLE IF NOT EXISTS plan AS SELECT * FROM plans_db.plans;
''')

# Commit changes and close the connections
conn_combined.commit()

# Detach the databases
cursor_combined.execute("DETACH DATABASE modules_db;")
cursor_combined.execute("DETACH DATABASE plans_db;")

# Close the combined.db connection
conn_combined.close()

print(f"Combined database created successfully as '{combined_db}' with 'modules' and 'plans' tables.")
