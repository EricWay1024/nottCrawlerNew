import requests
from bs4 import BeautifulSoup
import re
from common import ge, gh, gt
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from module.config import MODULE_SCHEMA, YEAR, RETRY_NUM
from module.util import get_mycode
from module.database import init_db, module_exists, insert_module
from retry import retry
from common import load_or_fetch
from module.config import SCHOOLS_PATH
import concurrent.futures
import queue
import threading
from module.fetch_brief import get_all_schools


db_queue = queue.Queue()
fetched_count = [0]
count_lock = threading.Lock()


def db_writer():
    conn, cursor = init_db()
    while True:
        module = db_queue.get()
        if module is None:  # Sentinel value to shut down the thread
            break
        insert_module(cursor, module)  # Insert module into SQLite
        conn.commit()
    conn.close()


# Example headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


@retry(tries=RETRY_NUM)
def get_modules_from_list(soup, campus, school):
    # Find all 'tr' elements with the class 'ps_grid-row'
    rows = soup.find_all("tr", class_="ps_grid-row")

    # List to store module information
    modules_info = []

    # Iterate through each 'tr' row and extract module information
    for i, row in enumerate(rows):
        # Extract the course code
        course_code = row.find(
            "a", id=lambda x: x and x.startswith("ADDRESS_LINK")
        ).text.strip()

        # Extract the course title
        course_title_div = row.find(
            "div",
            id=lambda x: x
            and x.startswith("win0divUN_PLN_EXT2_WRK_COURSE_TITLE_LONG"),
        )
        course_title = (
            course_title_div.find("p").text.strip()
            if course_title_div
            else "N/A"
        )

        # Extract the level
        level = row.find(
            "a", id=lambda x: x and x.startswith("UN_LEVEL2")
        ).text.strip()

        # Extract the term
        term = row.find(
            "span", id=lambda x: x and x.startswith("SSR_CRSE_TYPOFF_DESCR")
        ).text.strip()

        # Append the extracted information as a dictionary
        modules_info.append(
            {
                "index": i,
                "code": course_code,
                "title": course_title,
                "level": level,
                "term": term,
                "campus": campus,
                "school": school,
                "year": YEAR,
            }
        )
    return modules_info


@retry(tries=RETRY_NUM)
def get_module_link(session, icsid, index):
    data = {
        "ICAJAX": "1",
        "ICStateNum": "1",
        "ICAction": f"ADDRESS_LINK${index}",
        "ICSID": icsid,
    }
    response = session.post(
        "https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL",
        data=data,
    )
    # Regex to extract the link
    pattern = r"document\.location='(/psp/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT\.[^']+)'"
    # Searching for the link in the HTML
    match = re.search(pattern, response.text)
    # Extracting and printing the link
    link = match.group(1) if match else None
    return link


@retry(tries=RETRY_NUM)
def parse_module_page(link, campus, school_code, school_name, mycode):
    # Regex to extract CRSEID
    pattern = r"CRSEID=(\d+)"
    # Search for the pattern in the URL
    match = re.search(pattern, link)
    crseid = match.group(1)

    response = requests.get("https://campus.nottingham.ac.uk" + link)
    soup = BeautifulSoup(response.text, "html.parser")

    def ge_(i):
        return ge(soup, i)

    def gh_(i):
        return gh(soup, i)

    def gt_(id, headers):
        id_soup = soup.find(id=id)
        if id_soup is None:
            return []
        return gt(id_soup, headers)
    
    def clean_number_str(num_str: str) -> str:
        # If there’s a decimal point, strip trailing zeros...
        if "." in num_str:
            num_str = num_str.rstrip("0").rstrip(".")
        return num_str

    module_res = {
        "mycode": mycode,
        "courseId": crseid,
        "campus": campus,
        "year": ge_("UN_PLN_EXT2_WRK_ACAD_YEAR"),
        "code": ge_("UN_PLN_EXT2_WRK_SUBJECT_DESCR"),
        "title": ge_("UN_PLN_EXT2_WRK_PTS_LIST_TITLE"),
        "credits": clean_number_str(ge_("UN_PLN_EXT2_WRK_UNITS_MINIMUM")),
        "level": ge_("UN_PLN_EXT2_WRK_UN_LEVEL"),
        "summary": gh_("win0divUN_PLN_EXT2_WRK_HTMLAREA11"),
        "aims": gh_("win0divUN_PLN_EXT2_WRK_HTMLAREA12"),
        "offering": ge_("UN_PLN_EXT2_WRK_DESCRFORMAL"),
        "convenor": ge_("UN_PLN_EXT2_WRK_NAME_DISPLAYS_AS"),
        "semester": ge_("UN_PLN_EXT2_WRK_UN_TRIGGER_NAMES"),
        "requisites": gt_("win0divUN_PRECORQ9_TBL$grid$0", ["code", "title"]),
        "additionalRequirements": gt_(
            "win0divUN_ADD_REQ_CRSgridc-right$0", ["operator", "condition"]
        ),
        "outcome": gh_("UN_PLN_EXT2_WRK_UN_LEARN_OUTCOME"),
        "targetStudents": ge_("win0divUN_PLN_EXT2_WRK_HTMLAREA10"),
        "assessmentPeriod": ge_("win0divUN_PLN_EXT2_WRK_UN_DESCRFORMAL"),
        "class": gt_(
            "win0divUN_PRCS_FRQ_VWgridc-right$0",
            ["activity", "numOfWeeks", "numOfSessions", "sessionDuration"],
        ),
        "assessment": gt_(
            "win0divUN_CRS_ASAI_TBL$grid$0",
            ["assessment", "weight", "type", "duration", "requirements"],
        ),
        "belongsTo": {
            "code": school_code,
            "name": school_name,
            "campus": campus,
        },
        "corequisites": gt_("win0divUN_COCORQ9_TBLgridc$0", ["code", "title"]),
        "classComment": ge_("win0divUN_PLN_EXT2_WRK_UN_ACTIVITY_INFO"),
    }

    try:
        validate(
            instance=module_res,
            schema=MODULE_SCHEMA,
        )
    except ValidationError as e:
        print(
            "JSON schema validation error for module "
            f'{module_res["code"]} (courseId = {crseid}):'
        )
        print(e)

    return module_res


def process_module(session, icsid, module_obj, campus, school, school_name):
    index = module_obj["index"]
    link = get_module_link(session, icsid, index)
    if link is None:
        print(f'No link found in {module_obj["code"]}, pass...')
        return
    module = parse_module_page(
        link, campus, school, school_name, get_mycode(module_obj)
    )
    db_queue.put(module)


@retry(tries=RETRY_NUM)
def get_icsid(session, school, campus):
    response = session.get(
        f"https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PAGE=UN_CRS_EXT2_FPG&CAMPUS={campus}&TYPE=Module&YEAR={YEAR}&TITLE=&Module=&SCHOOL={school}&LINKA=",
        headers=headers,
    )
    soup = BeautifulSoup(response.text, "html.parser")
    element = soup.find(id="ICSID")
    icsid = element.get("value")
    return soup, icsid


def get_module_details(school, campus, school_name, fetched_count):
    conn, cursor = init_db()
    session = requests.Session()
    soup, icsid = get_icsid(session, school, campus)
    modules_info = get_modules_from_list(soup, campus, school)

    unfeteched_modules_info = []
    for module_obj in modules_info:
        if not module_exists(cursor, module_obj):
            unfeteched_modules_info.append(module_obj)
    conn.close()
    with count_lock:
        fetched_count[0] += len(modules_info) - len(unfeteched_modules_info)

    with concurrent.futures.ThreadPoolExecutor() as module_executor:
        future_to_module = {
            module_executor.submit(
                process_module,
                session,
                icsid,
                module_obj,
                campus,
                school,
                school_name,
            ): module_obj
            for module_obj in unfeteched_modules_info
        }

        for future in concurrent.futures.as_completed(future_to_module):
            try:
                future.result()
                with count_lock:
                    fetched_count[0] += 1
                    print(f"Fetched {fetched_count[0]} modules", end="\r")
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                print(f"Generated an exception: {exc}")

    conn.close()


if __name__ == "__main__":
    schools = load_or_fetch(SCHOOLS_PATH, get_all_schools)
    db_thread = threading.Thread(target=db_writer)
    db_thread.start()

    # Use ThreadPoolExecutor to handle the tasks concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit all the plans to the executor for concurrent processing
        futures = [
            executor.submit(
                get_module_details,
                s["code"],
                s["campus"],
                s["name"],
                fetched_count,
            )
            for s in schools
            if s["name"] != "United Kingdom"
        ]
        # Ensure all threads finish
        for future in concurrent.futures.as_completed(futures):
            try:
                # This will raise any exceptions encountered during execution
                future.result()
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                print(f"Generated an exception: {exc}")

    # Signal the db_writer thread to stop by putting a sentinel value in the queue
    db_queue.put(None)

    # Wait for the db_writer thread to finish
    db_thread.join()
