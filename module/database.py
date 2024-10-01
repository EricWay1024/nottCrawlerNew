from .config import DB_PATH
import sqlite3
import json
from .util import get_mycode
from .config import COURSE_TABLE_NAME

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f'''
    CREATE TABLE IF NOT EXISTS {COURSE_TABLE_NAME} (
        mycode TEXT  PRIMARY KEY ,
        code TEXT,
        semester TEXT,
        year TEXT,
        campus TEXT,
        title TEXT,
        credits REAL,
        level REAL,
        summary TEXT,
        aims TEXT,
        offering TEXT,
        convenor TEXT,
        requisites TEXT,
        additionalRequirements TEXT,
        outcome TEXT,
        targetStudents TEXT,
        assessmentPeriod TEXT,
        class TEXT,
        assessment TEXT,
        belongsTo TEXT,
        corequisites TEXT,
        classComment TEXT
    )
    ''')
    conn.commit()
    return conn, cur



# Function to insert a module into the database
def insert_module(cursor, module):
    cursor.execute(f'''
    INSERT OR REPLACE INTO {COURSE_TABLE_NAME} (
        mycode, code, semester, year, campus,
        title, credits, level, summary, aims, offering, convenor,
        requisites, additionalRequirements, outcome, targetStudents, assessmentPeriod,
         class, assessment, belongsTo, corequisites, classComment
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        module["mycode"],
        module["code"], module["semester"], module["year"], 
        module['campus'],
        module["title"], 
        module["credits"], module["level"],
        module["summary"], module["aims"], module["offering"], module["convenor"],
        json.dumps(module["requisites"]), 
        json.dumps(module["additionalRequirements"]),
        module["outcome"], 
        module["targetStudents"], 
        module["assessmentPeriod"], 
        json.dumps(module["class"]), 
        json.dumps(module["assessment"]), 
        json.dumps(module["belongsTo"]),
        json.dumps(module["corequisites"]), 
        module["classComment"],
    ))


def module_exists(cursor, module_obj):
    mycode = get_mycode(module_obj=module_obj)
    query = f"SELECT 1 FROM {COURSE_TABLE_NAME} WHERE mycode = ?"
    cursor.execute(query, (mycode, ))
    return cursor.fetchone() is not None