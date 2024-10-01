import sqlite3
from pathlib import Path
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
from retry import retry

THREADS = 1
HEADLESS = False

# Define the path to chromedriver.exe
driver_path = 'C:\\Users\\eric\\apps\\chromedriver.exe'

# Define Chrome options
options = Options()
if HEADLESS:
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

# Initialize the Chrome WebDriver service
service = Service(driver_path)

# Load the school and module data
schools = json.load(open("./res/schools.json"))
school_map = {o["code"]: o for o in schools}
module_objs = json.load(open("./res/module_brief.json"))

# Filter out modules from schools named 'United Kingdom'
module_objs = [m for m in module_objs if m["school"] != 'UNUK']

# Define the database name and path
db_path = Path('./res/modules.db')

# Initialize the SQLite connection


def init_db(mode):
    if mode == "scratch" and db_path.exists():
        db_path.unlink()  # Delete the existing database if in scratch mode

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS modules (
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
    cursor.execute('''
    INSERT OR REPLACE INTO modules (
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


def wait_until_element(browser, id, timeout=10):
    wait = WebDriverWait(browser, timeout)
    wait.until(
        EC.presence_of_element_located((By.ID, id))
    )

def get_mycode(module_obj):
    campus = module_obj["campus"]
    year = module_obj["year"]
    school = module_obj["school"]
    index = module_obj["index"]
    mycode = f"{school}_{index}_{year}_{campus}"
    return mycode


@retry(tries=5)
def get_module(browser, module_obj, school_map):
    campus = module_obj["campus"]
    year = module_obj["year"]
    school = module_obj["school"]
    index = module_obj["index"]

    mycode = get_mycode(module_obj)

    school_obj = school_map[school]

    browser.get(
        f"https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/"
        f"UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PAGE="
        f"UN_CRS_EXT2_FPG&"
        f"CAMPUS={campus}&TYPE=Module&YEAR={year}&TITLE=&Module=&"
        f"SCHOOL={school}&LINKA=&CAMPUS={campus}&TYPE=Module&YEAR={year}..."
    )

    wait_until_element(browser, "win0divUN_PCRSE_TBLgridc$0")
    rows = browser.find_elements(By.CLASS_NAME, 'ps_grid-row')
    rows[index].click()
    wait_until_element(browser, "UN_PLN_EXT2_WRK_ACAD_YEAR")

    def ge(id, desired_type=str):
        try:
            return desired_type(browser.find_element(By.ID, id).text.strip())
        except (NoSuchElementException, ValueError):
            return "" if desired_type == str else float('nan')

    def gh(id):
        try:
            return browser.find_element(By.ID, id).get_attribute('innerHTML')
        except NoSuchElementException:
            return ""

    def gt(div_id, headers):
        try:
            table_element = browser.find_element(By.ID, div_id)
        except NoSuchElementException:
            return []

        rows_data = []

        for row in table_element.find_elements(By.CSS_SELECTOR, "tbody tr"):
            row_data = {}
            cells = row.find_elements(By.CSS_SELECTOR, 'td:not(.ptgrid-rownumber)')
            for header, cell in zip(headers, cells):
                row_data[header] = cell.text.strip()
            rows_data.append(row_data)

        return rows_data

    return {
        "mycode": mycode,
        "campus": campus,
        "year": ge("UN_PLN_EXT2_WRK_ACAD_YEAR"),
        "code": ge("UN_PLN_EXT2_WRK_SUBJECT_DESCR"),
        "title": ge("UN_PLN_EXT2_WRK_PTS_LIST_TITLE"),
        "credits": ge("UN_PLN_EXT2_WRK_UNITS_MINIMUM", float),
        "level": ge("UN_PLN_EXT2_WRK_UN_LEVEL", float),
        "summary": gh("win0divUN_PLN_EXT2_WRK_HTMLAREA11"),
        "aims": gh("win0divUN_PLN_EXT2_WRK_HTMLAREA12"),
        "offering": ge("UN_PLN_EXT2_WRK_DESCRFORMAL"),
        "convenor": ge("UN_PLN_EXT2_WRK_NAME_DISPLAYS_AS"),
        "semester": ge("UN_PLN_EXT2_WRK_UN_TRIGGER_NAMES"),
        "requisites": gt("win0divUN_PRECORQ9_TBL$grid$0", 
                         ["code", "title"]),
                        #  {"Code": "subject", "Title": "courseTitle"}),
        "additionalRequirements": gt("win0divUN_ADD_REQ_CRSgridc-right$0", 
                                     ["operator", "condition"]),
                                    #  {"Operator": "operator", "Condition": "condition"}),
        "outcome": gh("UN_PLN_EXT2_WRK_UN_LEARN_OUTCOME"),
        "targetStudents": ge("win0divUN_PLN_EXT2_WRK_HTMLAREA10"),
        "assessmentPeriod": ge("win0divUN_PLN_EXT2_WRK_UN_DESCRFORMAL"),
        "class": gt("win0divUN_PRCS_FRQ_VWgridc-right$0", 
                    ["activity", "numOfWeeks", "numOfSessions", "sessionDuration"]),
                    # {"Course Component": "activity", "Number of weeks": "numOfWeeks", "Number of sessions": "numOfSessions", "Duration of a session": "sessionDuration"}),
        "assessment": gt("win0divUN_CRS_ASAI_TBL$grid$0", 
                         ["assessment", "weight", "type", "duration",  "requirements"]),
                        #  {"Assessment": "assessment", "Weight": "weight", "Type": "type", "Duration": "duration", "Requirements": "requirements"}),
        "belongsTo": school_obj,
        "corequisites": gt("win0divUN_COCORQ9_TBLgridc$0", 
                           ["code", "title"]),
                        #    {"Code": "subject", "Title": "courseTitle"}),
        "classComment": ge("win0divUN_PLN_EXT2_WRK_UN_ACTIVITY_INFO"),
    }


def init_browser():
    return webdriver.Chrome(service=service, options=options)


# Modify fetch function to use database interaction


# @retry(tries=2)
def fetch_modules_in_thread(modules_list, school_map, fetch_mode, fetched_count):
    driver = init_browser()  # Initialize the WebDriver once for each thread
    conn, cursor = init_db(fetch_mode)  # Initialize the database connection
    thread_modules = []  # Store results for this thread
    for module_obj in modules_list:
        try:
            module = get_module(driver, module_obj, school_map)
        except InvalidSessionIdException:
            driver = init_browser()
            module = get_module(driver, module_obj, school_map)

        insert_module(cursor, module)  # Insert module into SQLite
        conn.commit()  # Save all changes to the database
        thread_modules.append(module)

        # Increment fetched count and print progress
        fetched_count[0] += 1  # Using a mutable object (list) to keep track across threads
        print(f"Fetched {fetched_count[0]}/{len(module_objs)} modules", end='\r')
    driver.quit()
    conn.commit()  # Save all changes to the database
    conn.close()  # Close the database connection
    return thread_modules


# Main execution function

def run_fetch(mode="scratch"):
    conn, cursor = init_db(mode)

    if mode == "existing":
        # Function to get all existing module from the database
        cursor.execute('SELECT mycode FROM modules')
        exisitng_module_mycodes = {row[0] for row in cursor.fetchall()}
        # Remove the already existing modules from the list to avoid fetching them again
        filtered_modules = [
            module for module in module_objs
            if get_mycode(module) not in exisitng_module_mycodes
        ]
    else:
        filtered_modules = module_objs

    conn.close()
    all_modules = []  # List to store the concatenated results from all threads
    total_modules = len(filtered_modules)  # Get the total number of modules to fetch
    fetched_count = [len(exisitng_module_mycodes)]  # Use a list to keep track of fetched modules

    max_threads = THREADS
    modules_per_thread = total_modules // max_threads + 1
    modules_split = [filtered_modules[i:i + modules_per_thread] for i in range(0, total_modules, modules_per_thread)]

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_thread = {
            executor.submit(fetch_modules_in_thread, module_chunk, school_map, mode, fetched_count): idx
            for idx, module_chunk in enumerate(modules_split)
        }

        for future in as_completed(future_to_thread):
            thread_index = future_to_thread[future]
            try:
                thread_modules = future.result()
                all_modules.extend(thread_modules)
            except KeyboardInterrupt:
                raise
            # except Exception as e:
                # print(f"An error occurred in thread {thread_index}: {e}")
    print("\nAll modules have been fetched and saved to the database.")


# Example usage:
# run_fetch(mode="scratch")  # For scratch mode
run_fetch(mode="existing")  # For fetching only new modules

# driver = init_browser()
# s = get_module(driver,
#     {"campus": "U", "year": "2024", "school": "USC-MATH", "index": 1, "code": "MATH3004", "title": "Game Theory", "level": "3", "term": "Spring UK"}, 
#     school_map)
# from pprint import pprint
# pprint(s)