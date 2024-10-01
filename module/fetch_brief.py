import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from retry import retry

def get_schools_from_campus(campus):
    params = {
        'PAGE': 'UN_PLN_EXT1_FPG',
        'CAMPUS': campus,
        'TYPE': 'Module',
    }

    response = requests.get(
        'https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL',
        params=params,
        # cookies=cookies,
        # headers=headers,
    )

    module_soup = BeautifulSoup(response.text, "html.parser")

    # Find the select element by its ID
    select_element = module_soup.find('select',
                                      id='UN_PLN_EXRT_WRK_DESCRFORMAL')

    # Extract all the option elements within the select
    options = select_element.find_all('option')

    # Create a list to store the schools and their values
    schools = []

    # Iterate through each option and extract the value and text
    for option in options:
        school_value = option.get('value').strip()
        school_name = option.text.strip()
        # Exclude the default empty option
        if school_value:
            schools.append({
                "code": school_value,
                "name": school_name,
                'campus': campus,
            })
    return schools


def get_all_schools():
    res = []
    for campus in ['C', 'M', 'U']:
        res.extend(get_schools_from_campus(campus))
    return res


@retry(tries=5)
def get_modules_from_school(school, campus='U', year='2024'):
    # The URL to request
    url = "https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL"
    # Parameters to be included in the request
    params = {
        'PAGE': 'UN_CRS_EXT2_FPG',
        'CAMPUS': campus,
        'TYPE': 'Module',
        'YEAR': year,
        'TITLE': '',
        'Module': '',
        'SCHOOL': school,
        'LINKA': '',
    }

    # Sending the GET request
    response = requests.get(url, params=params)

    # Assuming response.text contains the HTML content
    html_content = response.text

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all 'tr' elements with the class 'ps_grid-row'
    rows = soup.find_all('tr', class_='ps_grid-row')

    # List to store module information
    modules_info = []

    # Iterate through each 'tr' row and extract module information
    for i, row in enumerate(rows):
        # Extract the course code
        course_code = row.find('a', id=lambda x: x and x.startswith('ADDRESS_LINK')).text.strip()

        # Extract the course title
        course_title_div = row.find('div', id=lambda x: x and x.startswith('win0divUN_PLN_EXT2_WRK_COURSE_TITLE_LONG'))
        course_title = course_title_div.find('p').text.strip() if course_title_div else "N/A"

        # Extract the level
        level = row.find('a', id=lambda x: x and x.startswith('UN_LEVEL2')).text.strip()

        # Extract the term
        term = row.find('span', id=lambda x: x and x.startswith('SSR_CRSE_TYPOFF_DESCR')).text.strip()

        # Append the extracted information as a dictionary
        modules_info.append({
            'campus': campus,
            'year': year,
            'school': school,
            'index': i,
            'code': course_code,
            'title': course_title,
            'level': level,
            'term': term,
        })
    return modules_info


try:
    schools = json.load(open("./res/schools.json"))
except FileNotFoundError:
    schools = get_all_schools()
    json.dump(schools, open("res/schools.json", "w"))

all_modules = []
for school in tqdm(schools):
    modules = get_modules_from_school(school["code"], campus=school['campus'])
    all_modules.extend(modules)

json.dump(all_modules, open("res/module_brief.json", "w"))
