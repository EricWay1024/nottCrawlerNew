
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Define Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
# Add more options here if needed

# Define paths
user_home_dir = os.path.expanduser("~")
chrome_binary_path = os.path.join(user_home_dir, "chrome-linux64", "chrome")
chromedriver_path = os.path.join(user_home_dir, "chromedriver-linux64", "chromedriver")

# Set binary location and service
chrome_options.binary_location = chrome_binary_path
service = Service(chromedriver_path)

# Initialize Chrome WebDriver
browser = webdriver.Chrome(service=service, options=chrome_options)
browser.implicitly_wait(10)


def get_school(school, campus='U', year='2024'):
    browser.get(f"https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PAGE=UN_CRS_EXT2_FPG&CAMPUS={campus}&TYPE=Module&YEAR={year}&TITLE=&Module=&SCHOOL={school}&LINKA=&CAMPUS={campus}&TYPE=Module&YEAR={year}&TITLE=&Module=&SCHOOL={school}")

    rows = browser.find_elements(By.CLASS_NAME, 'ps_grid-row')
    rows[0].click()

    module_info = {}

    def ge(id):
        return browser.find_element(By.ID, id).text.strip()

    def extract_table_data_by_div_id(driver, div_id):
        """
        Extracts table data from a div element containing a single table, given the div's ID.
        
        Args:
            driver (webdriver.Chrome): The Selenium WebDriver instance.
            div_id (str): The ID of the div element containing the table.

        Returns:
            List[Dict]: A list of dictionaries representing the table data, where each
                        dictionary corresponds to a row and the keys are the table headers.
        """
        # Locate the table within the specified div element by ID
        table_element = driver.find_element(By.ID, div_id)
        
        # Extract the headers from the table
        headers = []
        header_elements = table_element.find_elements(By.CSS_SELECTOR, "thead th")
        for header in header_elements:
            headers.append(header.text.strip())
        
        # Extract the rows of the table
        rows_data = []
        rows = table_element.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in rows:
            row_data = {}
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            for header, cell in zip(headers, cells):
                row_data[header] = cell.text.strip()
            rows_data.append(row_data)
        
        return rows_data
    
    module_info = {
        "year": ge("UN_PLN_EXT2_WRK_ACAD_YEAR"),
        "code": ge("UN_PLN_EXT2_WRK_SUBJECT_DESCR"),
        "title": ge("UN_PLN_EXT2_WRK_PTS_LIST_TITLE"),
        "credits": ge("UN_PLN_EXT2_WRK_UNITS_MINIMUM"),
        "level": ge("UN_PLN_EXT2_WRK_UN_LEVEL"),
        "summary": ge("win0divUN_PLN_EXT2_WRK_HTMLAREA11"), # TODO
        "aims": ge("win0divUN_PLN_EXT2_WRK_HTMLAREA12"), #TODO
        "offering": ge("UN_PLN_EXT2_WRK_DESCRFORMAL"),
        "convenor": ge("UN_PLN_EXT2_WRK_NAME_DISPLAYS_AS"),
        "semester": ge("UN_PLN_EXT2_WRK_UN_TRIGGER_NAMES"),
        "requisites": None,
        "additionalRequirements": None,
        "outcome": None,
        "targetStudents": None,
        "assessmentPeriod": None,
        "courseWebLinks": None,
        "class": None,
        "assessment": None,
        "belongsTo": None

    }
    print(module_info)
    

get_school("USC-ABE")
# browser.close()
