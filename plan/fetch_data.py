import requests
from bs4 import BeautifulSoup
from re import compile as rc
import re
from retry import retry
from .util import get_degree_info


def get_all_plans(campus, year):
    # URL to fetch the HTML content
    url = f'https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PAGE=UN_PLN_EXT2_FPG&CAMPUS={campus}&TYPE=Programme&YEAR={year}&TITLE=&PLAN=&UCAS='

    # Fetch the HTML content
    response = requests.get(url)

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <tr> elements with class 'ps_grid-row' which represent each plan row
    rows = soup.find_all('tr', class_='ps_grid-row')

    # Loop through the rows and extract the relevant plan information
    plan_info_list = []

    for row in rows:
        # Extract the Plan Code (DESCRSHORT)
        plan_code = row.find('span', id=lambda x: x and x.startswith('UN_PAM_PLN_TBL_DESCRSHORT')).get_text(strip=True)
        
        # Extract the Link Code (e.g., U6UMTHPY, U7UMTHPY)
        link_code = row.find('a', id=lambda x: x and x.startswith('HYPERLINK')).get_text(strip=True)
        
        # Extract the Plan Description (e.g., BSc Hons Mathematical Physics)
        plan_desc = row.find('span', id=lambda x: x and x.startswith('UN_PAM_PLN_TBL_TRNSCR_DESCR')).get_text(strip=True)
        
        # Extract additional Notes (e.g., U6UMTHPY (UCAS:F326))
        notes = row.find('span', id=lambda x: x and x.startswith('UN_PLN_EXT2_WRK_DESCRLONG_NOTES')).get_text(strip=True)
        
        # Store all the extracted info into a dictionary
        plan_info = {
            'ucas': plan_code,
            'code': link_code,
            'title': plan_desc,
            'notes': notes,
            'campus': campus,
            'year': year,
        }
        
        # Append the plan info to the list
        plan_info_list.append(plan_info)
    
    return plan_info_list


def replace_spaces(text):
    # This regex will match one or more consecutive whitespace characters (including newlines)
    return re.sub(r'\s+', ' ', text).strip()

# Get text or number from element with id
def ge(soup, id, desired_type=str):
    try:
        element = soup.find(id=id)
        return desired_type(replace_spaces(element.get_text(strip=True)))
    except (AttributeError, ValueError):
        return "" if desired_type == str else float('nan')


# Get HTML from element with id
def gh(soup, id):
    try:
        element = soup.find(id=id)
        return replace_spaces(element.decode_contents()) if element else ""
    except AttributeError:
        return ""

# Get a table from element with id
def gt(soup, headers):
    rows_data = []
    # Find all rows in the table (assuming they are in the <tbody> under <tr>)
    for row in soup.select("tbody tr"):
        row_data = {}
        # Find all cells in the row that are not row number cells
        cells = row.find_all('td')
        for header, cell in zip(headers, cells):
            row_data[header] = replace_spaces(cell.get_text(strip=True))
        rows_data.append(row_data)
    return rows_data


def parse_modules(soup):
    def get_modules_from_group(group_soup):
        return gt(
            group_soup,
            ['code', 'title', 'credits', 'compensatable', 'taught'],
        )

    def process_group(group_soup, type):
        ge_ = lambda p: ge(group_soup, rc(p))
        res = {
            'type': type,
            'modules': get_modules_from_group(group_soup),
        }
        if type == 'Compulsory':
            return {
                'title': ge_(r'^UN_PAM_PLAN_WRK_UN_PAM_COMPULSORY\$\d+lbl$'),
                'message': ge_(r'^win0div\$ICField509\$\d+$'),
                **res,
            }
        elif type == 'Restricted':
            return {
                'title': ge_(r'^win0divUN_PAM_RES_TBL_DESCR50\$\d+$'),
                'message': ge_(r'^win0divUN_PAM_PLAN_WRK_UN_RESTRICT_MSG\$\d+$'),
                **res,
            }
        elif type == "Alternative":
            return {
                'title': ge_(r'^win0divUN_PAM_ALTR_TBL_DESCR50\$\d+$'),
                'message': ge_(r'^win0divUN_PAM_PLAN_WRK_UN_ALTER_MSG\$\d+$'),
                **res,
            }
        else:
            raise ValueError("Invalid group type. Must be Compulsory, Restricted or Alternative.")

    def is_empty_group(group_obj):
        return group_obj['message'] == '' and \
            group_obj['title'] == '' and \
            group_obj['modules'] == []

    def get_all_groups_from_year(year_soup):
        comp_groups = year_soup.find_all(id=rc(r'^win0divUN_PAM_PLAN_WRK_UN_PAM_COMPULSORY\$\d+$'))
        rest_groups = year_soup.find_all(id=rc(r'^win0divUN_PAM_RES_TBL_row\$\d+$'))
        altr_groups = year_soup.find_all(id=rc(r'^win0divUN_PAM_ALTR_TBL_row\$\d+$'))
        return list(filter(lambda g: not is_empty_group(g), 
                            [process_group(g, 'Compulsory') for g in comp_groups] + \
                            [process_group(g, 'Restricted') for g in rest_groups] + \
                            [process_group(g, 'Alternative') for g in altr_groups]))
    
    years = soup.find_all(id=rc(r'^win0divUN_PAMPEAM_TBL_row\$\d+$'))
    res = []
    for year_index, year_soup in enumerate(years):
        year_obj = {
            "title": ge(year_soup, f'UN_PAMPEAM_TBL_DESCR50${year_index}'),
            "groups": get_all_groups_from_year(year_soup),
            "additionalCourseChoice": ge(year_soup, rc(r'^win0divUN_PAM_ADDT_TBL_SSR_INSTRCTN_LONG\$\d+$')),
        }
        res.append(year_obj)
    return res


@retry(tries=5)
def get_plan(plan_code, year, campus):
    response = requests.get(f'https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PAGE=UN_PLN_EXT3_FPG&CAMPUS={campus}&TYPE=Programme&YEAR={year}&TITLE=UON-e&PLAN={plan_code}&UCAS=', timeout=10) 
    soup = BeautifulSoup(response.text, 'html.parser')
    # soup = BeautifulSoup(open("m.html", "r", encoding="utf-8").read(), 'html.parser')  # TODO testing only
    modules = parse_modules(soup)

    ge_ = lambda id: ge(soup, id)
    gh_ = lambda id: gh(soup, id)

    plan_title = ge_("UN_PAM_EXTR_WRK_DESCR200")
    degree_info = get_degree_info(plan_title)

    return {
        "title": plan_title,
        **degree_info,  # degreeType and degree
        "year": year,
        "campus": campus,
        "academicPlanCode": ge_("UN_PPLN_DTL_TBL_ACAD_PLAN$22$"),
        "ucasCode": ge_("UN_PAM_EXTR_WRK_DESCRSHORT1$313$"),
        "school": ge_("UN_PLN_EXT2_WRK_SCH_DAILY_DETAIL"),
        "planType": ge_("UN_PPLN_DTL_TBL_UN_PLAN_TYPE"),
        # "academicLoad": ge_(),
        "deliveryMode": ge_("UN_PLN_EXT2_WRK_DESCR40$369$"),
        "duration": ge_("UN_PPLN_DTL_TBL_UN_DEPTDESCR$503$"),

        "subjectBenchmark": ge_("win0divUN_PLN_EXT2_WRK_DESCRLONG1"),
        "planAccreditation": gh_("win0divUN_PLN_EXT2_WRK_DESCRLONG2"),

        "educationalAimsIntro": gh_("UN_PPLN_DTL_TBL_UN_INTRODUCTION"),
        "educationalAims": gh_("win0div$ICField467$0"),

        "outlineDescription": gh_("UN_PPLN_DTL_TBL_UN_OUTLN_DESC_PGM"),

        "distinguishingFeatures": gh_("win0divUN_PPLN_DTL_TBL_UN_DISTINGSH_FEATU$73$"),

        # "furtherInformation": ge_(),

        # admission requirements
        "planRequirements": ge_("UN_PPLN_DTL_TBL_UN_PLAN_RQMNTS"),
        "includingSubjects": ge_("UN_PPLN_DTL_TBL_UN_REQ_SUBJECTS"),
        "excludingSubjects": ge_("UN_PPLN_DTL_TBL_UN_EXCLUDE_SUBJECT"),
        "otherRequirements": ge_("UN_PPLN_DTL_TBL_UN_OTHER_REQ"),
        "ieltsRequirements": ge_("UN_PPLN_DTL_TBL_UN_IELTS"),
        "generalInformation": ge_("UN_PPLN_DTL_TBL_UN_GENERAL_INFO"),

        "modules": modules,

        # Assessment
        "assessment": gh_("win0divUN_PAM_EXTR_WRK_DESCRLONG$319$"),
        "assessmentMarking": gh_("win0div$ICField479grp"),
        "progressionInformation": gh_("UN_PPLN_DTL_TBL_UN_ASSMNT_PROG_REG$76$"),
        "borderlineCriteria": gh_("UN_PPLN_DTL_TBL_UN_BRDR_LN_DESCR$327$"),
        "degreeInformation": gh_("UN_PPLN_DTL_TBL_UN_ASSES_AWARD_REG$273$"),
        "courseWeightings": ge_("UN_PLN_EXT2_WRK_DESCR100A$435$"),
        "degreeCalculationModel": ge_("UN_PLN_EXT2_WRK_DESCRLONG"),

        "otherRegulations": ge_("UN_PPLN_DTL_TBL_UN_OTHER_REGULATN"),
        "additionalRegulations": ge_("UN_PPLN_DTL_TBL_UN_STANDNG_REGULTN$328$"),

        # Learning outcomes
        "learningOutcomes": gh_("win0div$ICField482"),
    }

    # https://github.com/EricWay1024/uCourse-crawler/blob/master/plan.js
