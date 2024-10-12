from .config import DB_PATH
import sqlite3
import json
from .util import get_mycode
from .config import COURSE_TABLE_NAME, MODULE_SCHEMA
from common import get_fields_from_schema

text_fields, obj_fields, all_fields = get_fields_from_schema(MODULE_SCHEMA)


def init_db():
    make_table_script = (
        f"CREATE TABLE IF NOT EXISTS {COURSE_TABLE_NAME} (\n"
        + ",\n".join([f"  {field} TEXT" for field in all_fields])
        + ",\n  PRIMARY KEY (mycode)); "
    )
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(make_table_script)
    conn.commit()
    return conn, cur


# Function to insert a module into the database
def insert_module(cursor, module):
    # Prepare the insert query
    insert_query = (
        f"INSERT INTO {COURSE_TABLE_NAME} ("
        + ",\n".join(all_fields)
        + ") VALUES ("
        + ", ".join(["?" for _ in all_fields])
        + ")"
    )
    insert_tuple = tuple(
        [module[field] for field in text_fields]
        + [json.dumps(module[field]) for field in obj_fields]
    )
    # Insert the module data into the database
    cursor.execute(insert_query, insert_tuple)


def module_exists(cursor, module_obj):
    mycode = get_mycode(module_obj=module_obj)
    query = f"SELECT 1 FROM {COURSE_TABLE_NAME} WHERE mycode = ?"
    cursor.execute(query, (mycode,))
    return cursor.fetchone() is not None
