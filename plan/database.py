import sqlite3
import json
from .config import DB_PATH, PLAN_TABLE_NAME, PLAN_SCHEMA
from .util import get_fields_from_schema


text_fields, obj_fields, all_fields = get_fields_from_schema(PLAN_SCHEMA)


# Function to check if a plan already exists in the database
def plan_exists(cursor, year, campus, academicPlanCode):
    query = f"SELECT 1 FROM {PLAN_TABLE_NAME} WHERE year = ? AND campus = ? AND academicPlanCode = ?"
    cursor.execute(query, (year, campus, academicPlanCode))
    return cursor.fetchone() is not None


def insert_plan(cursor, plan_data):
    # Prepare the insert query
    insert_query = (
        f"INSERT INTO {PLAN_TABLE_NAME} ("
        + ",\n".join(all_fields)
        + ") VALUES ("
        + ", ".join(["?" for _ in all_fields])
        + ")"
    )
    insert_tuple = tuple(
        [plan_data[field] for field in text_fields]
        + [json.dumps(plan_data[field]) for field in obj_fields]
    )
    # Insert the plan data into the database
    cursor.execute(insert_query, insert_tuple)


# Create the SQLite table
def create_table():
    # SQL Script to create the table
    make_table_script = (
        f"CREATE TABLE IF NOT EXISTS {PLAN_TABLE_NAME} (\n"
        + ",\n".join([f"  {field} TEXT" for field in all_fields])
        + ",\n  PRIMARY KEY (year, campus, academicPlanCode)); "
    )
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(make_table_script)
    conn.commit()
    conn.close()
