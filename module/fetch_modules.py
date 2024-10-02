from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from retry import retry
from .util import get_mycode
from .database import init_db, insert_module, module_exists
from .config import THREADS, DRIVER_PATH, HEADLESS, MODULE_SCHEMA
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def wait_until_element(browser, id, timeout=10):
    wait = WebDriverWait(browser, timeout)
    wait.until(
        EC.presence_of_element_located((By.ID, id))
    )


@retry(tries=5)
def get_module(browser, module_obj):
    campus = module_obj["campus"]
    year = module_obj["year"]
    school = module_obj["school"]
    index = module_obj["index"]
    school_obj = module_obj["school_obj"]

    mycode = get_mycode(module_obj)

    browser.get(
        f"https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/"
        f"UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PAGE="
        f"UN_CRS_EXT2_FPG&"
        f"CAMPUS={campus}&TYPE=Module&YEAR={year}&TITLE=&Module=&"
        f"SCHOOL={school}&LINKA="
        # "&CAMPUS={campus}&TYPE=Module&YEAR={year}"
    )

    wait_until_element(browser, "win0divUN_PCRSE_TBLgridc$0")
    rows = browser.find_elements(By.CLASS_NAME, 'ps_grid-row')
    rows[index].click()
    wait_until_element(browser, "UN_PLN_EXT2_WRK_ACAD_YEAR")

    def ge(id):
        try:
            return browser.find_element(By.ID, id).text.strip()
        except NoSuchElementException:
            return ""

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

    module_res = {
        "mycode": mycode,
        "campus": campus,
        "year": ge("UN_PLN_EXT2_WRK_ACAD_YEAR"),
        "code": ge("UN_PLN_EXT2_WRK_SUBJECT_DESCR"),
        "title": ge("UN_PLN_EXT2_WRK_PTS_LIST_TITLE"),
        "credits": ge("UN_PLN_EXT2_WRK_UNITS_MINIMUM"),
        "level": ge("UN_PLN_EXT2_WRK_UN_LEVEL"),
        "summary": gh("win0divUN_PLN_EXT2_WRK_HTMLAREA11"),
        "aims": gh("win0divUN_PLN_EXT2_WRK_HTMLAREA12"),
        "offering": ge("UN_PLN_EXT2_WRK_DESCRFORMAL"),
        "convenor": ge("UN_PLN_EXT2_WRK_NAME_DISPLAYS_AS"),
        "semester": ge("UN_PLN_EXT2_WRK_UN_TRIGGER_NAMES"),
        "requisites": gt("win0divUN_PRECORQ9_TBL$grid$0", 
                         ["code", "title"]),
        "additionalRequirements": gt("win0divUN_ADD_REQ_CRSgridc-right$0", 
                                     ["operator", "condition"]),
        "outcome": gh("UN_PLN_EXT2_WRK_UN_LEARN_OUTCOME"),
        "targetStudents": ge("win0divUN_PLN_EXT2_WRK_HTMLAREA10"),
        "assessmentPeriod": ge("win0divUN_PLN_EXT2_WRK_UN_DESCRFORMAL"),
        "class": gt("win0divUN_PRCS_FRQ_VWgridc-right$0", 
                    ["activity", "numOfWeeks", "numOfSessions", "sessionDuration"]),
        "assessment": gt("win0divUN_CRS_ASAI_TBL$grid$0", 
                         ["assessment", "weight", "type", "duration",  "requirements"]),
        "belongsTo": school_obj,
        "corequisites": gt("win0divUN_COCORQ9_TBLgridc$0", 
                           ["code", "title"]),
        "classComment": ge("win0divUN_PLN_EXT2_WRK_UN_ACTIVITY_INFO"),
    }

    try:
        validate(
            instance=module_res,
            schema=MODULE_SCHEMA,
        )
    except ValidationError as e:
        print(f'JSON schema validation error for module {module_res["code"]} (mycode = {mycode}):')
        print(e)

    return module_res

def init_browser():
    # Define Chrome options
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
    # Initialize the Chrome WebDriver service
    service = Service(DRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)


# Modify fetch function to use database interaction
# We don't want to start a browser for each module (too slow),
# so each browser is responsible for a list of modules
def fetch_modules_in_thread(modules_list, fetched_count, total_count):
    driver = init_browser()  # Initialize the WebDriver once for each thread
    conn, cursor = init_db()  # Initialize the database connection
    for module_obj in modules_list:
        if module_exists(cursor, module_obj):
            fetched_count[0] += 1  # Using a mutable object (list) to keep track across threads
            print(f"Fetched {fetched_count[0]}/{total_count} modules", end='\r')
            continue
        try:
            module = get_module(driver, module_obj)
        except InvalidSessionIdException:  # If the brwoser died for some reason
            driver = init_browser()
            module = get_module(driver, module_obj)

        insert_module(cursor, module)  # Insert module into SQLite
        conn.commit()  # Save all changes to the database
        # Increment fetched count and print progress
        fetched_count[0] += 1  # Using a mutable object (list) to keep track across threads
        print(f"Fetched {fetched_count[0]}/{total_count} modules", end='\r')
    driver.quit()
    conn.commit()  # Save all changes to the database
    conn.close()  # Close the database connection

# Main execution function
def run_fetch(modules_list):
    total_count = len(modules_list)  # Get the total number of modules to fetch
    fetched_count = [0]  # Use a list to keep track of fetched modules

    # This is because we want the number of modules already fetched to be roughly
    # the same in each thread:
    random.shuffle(modules_list)

    modules_per_thread = total_count // THREADS + 1
    modules_split = [modules_list[i:i + modules_per_thread] for i in range(0, total_count, modules_per_thread)]

    errors_occured = False
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_thread = {
            executor.submit(fetch_modules_in_thread, module_chunk, fetched_count, total_count): idx
            for idx, module_chunk in enumerate(modules_split)
        }

        for future in as_completed(future_to_thread):
            thread_index = future_to_thread[future]
            try:
                future.result()
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"An error occurred in thread {thread_index}: {e}")
                errors_occured = True
    
    fetched_count = [0]
    if errors_occured:
        # Do the rest in single thread... maybe
        fetch_modules_in_thread(modules_list, fetched_count, total_count)

    print("\nAll modules have been fetched and saved to the database.")

