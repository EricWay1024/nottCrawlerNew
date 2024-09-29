
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from retry import retry
from tqdm import tqdm

# Define Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
# Add more options here if needed

# Define paths
user_home_dir = os.path.expanduser("~")
chrome_binary_path = os.path.join(user_home_dir, "chrome-linux64", "chrome")
chromedriver_path = os.path.join(
    user_home_dir, "chromedriver-linux64", "chromedriver")

# Set binary location and service
chrome_options.binary_location = chrome_binary_path
service = Service(chromedriver_path)

# Initialize Chrome WebDriver


def wait_until_element(browser, id, timeout=10):
    wait = WebDriverWait(browser, timeout)
    wait.until(
        EC.presence_of_element_located((By.ID, id))
    )


@retry()
def get_module(browser, module_obj, school_map):
    campus = module_obj["campus"]
    year = module_obj["year"]
    school = module_obj["school"]
    index = module_obj["index"]

    school_obj = school_map[school]

    browser.get(
        f"https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/"
        f"UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PAGE="
        f"UN_CRS_EXT2_FPG&"
        f"CAMPUS={campus}&TYPE=Module&YEAR={year}&TITLE=&Module=&"
        f"SCHOOL={school}&LINKA=&CAMPUS={campus}&TYPE=Module&YEAR={year}"
        f"&TITLE=&Module=&SCHOOL={school}")
    wait_until_element(browser, "win0divUN_PCRSE_TBLgridc$0")
    rows = browser.find_elements(By.CLASS_NAME, 'ps_grid-row')
    rows[index].click()
    wait_until_element(browser, "UN_PLN_EXT2_WRK_ACAD_YEAR")

    def ge(id, desired_type=str):
        try:
            res = desired_type(browser.find_element(By.ID, id).text.strip())
            return res
        except NoSuchElementException:
            return ""
        except ValueError:
            if desired_type in [float, int]:
                return float("nan")
            else:
                return ""

    def gh(id):
        try:
            return browser.find_element(By.ID, id).get_attribute('innerHTML')
        except NoSuchElementException:
            return ""

    def gt(div_id, header_map={}):
        """
        Extracts table data from a div element containing a single table,
        given the div's ID.

        Args:
            driver (webdriver.Chrome): The Selenium WebDriver instance.
            div_id (str): The ID of the div element containing the table.

        Returns:
            List[Dict]: A list of dictionaries representing the table data,
            where each
                        dictionary corresponds to a row and the keys are the
                        table headers.
        """
        # Locate the table within the specified div element by ID
        try:
            table_element = browser.find_element(By.ID, div_id)
        except NoSuchElementException:
            return []

        # Extract the headers from the table
        headers = []
        header_elements = table_element.find_elements(
            By.CSS_SELECTOR, "thead th")
        for header in header_elements:
            headers.append(header.text.strip())

        # Extract the rows of the table
        rows_data = []
        rows = table_element.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in rows:
            row_data = {}
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            for header, cell in zip(headers, cells):
                k, v = header, cell.text.strip()
                if k == '' and v == '':
                    continue
                if header_map.get(k) is not None:
                    k = header_map[k]
                row_data[k] = v
            rows_data.append(row_data)

        return rows_data

    return {
        "year": ge("UN_PLN_EXT2_WRK_ACAD_YEAR"),
        "code": ge("UN_PLN_EXT2_WRK_SUBJECT_DESCR"),
        "title": ge("UN_PLN_EXT2_WRK_PTS_LIST_TITLE"),
        "credits": ge("UN_PLN_EXT2_WRK_UNITS_MINIMUM", desired_type=float),
        "level": ge("UN_PLN_EXT2_WRK_UN_LEVEL", desired_type=float),
        "summary": gh("win0divUN_PLN_EXT2_WRK_HTMLAREA11"),
        "aims": gh("win0divUN_PLN_EXT2_WRK_HTMLAREA12"),
        "offering": ge("UN_PLN_EXT2_WRK_DESCRFORMAL"),
        "convenor": [{"name": ge("UN_PLN_EXT2_WRK_NAME_DISPLAYS_AS")}],
        "semester": ge("UN_PLN_EXT2_WRK_UN_TRIGGER_NAMES"),
        "requisites": gt("win0divUN_PRECORQ9_TBL$grid$0", header_map={
            "Code": "subject",  # sorry for this bad name
            "Title": "courseTitle",
        }),
        "additionalRequirements": gt("win0divUN_ADD_REQ_CRSgridc-right$0",
                                     header_map={
                                         'Operator': 'operator',
                                         'Condition': 'condition',
                                     }),
        "outcome": gh("UN_PLN_EXT2_WRK_UN_LEARN_OUTCOME"),
        "targetStudents": ge("win0divUN_PLN_EXT2_WRK_HTMLAREA10"),
        "assessmentPeriod": ge("win0divUN_PLN_EXT2_WRK_UN_DESCRFORMAL"),
        "courseWebLinks": [],
        "class": gt("win0divUN_PRCS_FRQ_VWgridc-right$0", header_map={
            "Course Component": "activity",
            "Number of weeks": "numOfWeeks",
            "Number of sessions": "numOfSessions",
            "Duration of a session": "sessionDuration",
        }),
        "assessment": gt("win0divUN_CRS_ASAI_TBL$grid$0", header_map={
            "Assessment": "assessment",
            "Weight": "weight",
            "Type": "type",
            "Duration": "duration",
            "Requirements": "requirements",
        }),
        "belongsTo": school_obj,

        "corequisites": gt("win0divUN_COCORQ9_TBLgridc$0", header_map={
            "Code": "subject",  # sorry for this bad name, again
            "Title": "courseTitle",
        }),
        "classComment": ge("win0divUN_PLN_EXT2_WRK_UN_ACTIVITY_INFO"),
    }


schools = json.load(open("./res/schools.json"))
school_map = {
    o["code"]: o for o in schools
}
module_objs = json.load(open("./res/module_brief.json"))


# Function to run get_school for a given school
@retry()
def fetch_module(module_obj):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        module = get_module(driver, module_obj, school_map)
    finally:
        driver.quit()  # Make sure to close the WebDriver
    return module


# List to store the concatenated results
all_modules = []

# Maximum number of threads
max_threads = 5

# Use ThreadPoolExecutor to run fetch_modules_for_school concurrently
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    # Submit tasks for each school
    future_to_module = {
        executor.submit(fetch_module, module_obj): module_obj["code"]
        for module_obj in module_objs}

    # Collect the results as they are completed
    for future in tqdm(as_completed(future_to_module), total=len(future_to_module)):
        module_code = future_to_module[future]
        try:
            module = future.result()
            with open(f"res/{module_code}.json", "w") as f:
                json.dump(module, f, indent=2)
            all_modules.append(module)  # Add all modules to the list
        except Exception as e:
            print(f"An error occurred for {module_code}: {e}")

# Save the concatenated list of all modules to a JSON file
with open("res/all_modules.json", "w") as f:
    json.dump(all_modules, f, indent=2)

print("All modules have been saved to all_modules.json")
