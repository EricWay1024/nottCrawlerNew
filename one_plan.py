import requests
from bs4 import BeautifulSoup
from re import compile as rc
import re

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
        return element.decode_contents() if element else ""
    except AttributeError:
        return ""

# Get a table from element with id
def gt(soup, div_id, headers):
    try:
        table_element = soup.find(id=div_id) if div_id is not None else soup
        if not table_element:
            return []
    except AttributeError:
        return []
    rows_data = []
    # Find all rows in the table (assuming they are in the <tbody> under <tr>)
    for row in table_element.select("tbody tr"):
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
            None,
            ['code', 'title', 'credits', 'compensatable', 'taught'],
        )

    def process_group(group_soup, type):
        res = {
            'type': type,
            'modules': get_modules_from_group(group_soup),
        }
        if type == 'Compulsory':
            return {
                'title': ge(group_soup, 
                            rc(r'^UN_PAM_PLAN_WRK_UN_PAM_COMPULSORY\$\d+lbl$')),
                'message': ge(group_soup,
                            rc(r'^win0div\$ICField509\$\d+$')),
                **res,
            }
        elif type == 'Restricted':
            return {
                'title': ge(group_soup,
                            rc(r'^win0divUN_PAM_RES_TBL_DESCR50\$\d+$')),
                'message': ge(group_soup,
                                rc(r'^win0divUN_PAM_PLAN_WRK_UN_RESTRICT_MSG\$\d+$')),
                **res,
            }
        elif type == "Alternative":
            return {
                'title': ge(group_soup,
                            rc(r'^win0divUN_PAM_ALTR_TBL_DESCR50\$\d+$')),
                'message': ge(group_soup,
                                rc(r'^win0divUN_PAM_PLAN_WRK_UN_ALTER_MSG\$\d+$')),
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

def get_plan(plan_code, year, campus):

    # response = requests.get(f'https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PAGE=UN_PLN_EXT3_FPG&CAMPUS={campus}&TYPE=Programme&YEAR={year}&TITLE=UON-e&PLAN={plan_code}&UCAS=') 
    # soup = BeautifulSoup(response.text, 'html.parser')
    soup = BeautifulSoup(open("m.html", "r", encoding="utf-8").read(), 'html.parser')  # TODO testing only
    modules = parse_modules(soup)

    ge_ = lambda id: ge(soup, id)

    return {
       {
        "title": ge_("UN_PAM_EXTR_WRK_DESCR200"),
        "academicPlanCode": ge_("UN_PPLN_DTL_TBL_ACAD_PLAN$22$"),
        "ucasCode": ge_("UN_PAM_EXTR_WRK_DESCRSHORT1$313$"),
        "school": ge_("UN_PLN_EXT2_WRK_SCH_DAILY_DETAIL"),
        "planType": ge_("UN_PPLN_DTL_TBL_UN_PLAN_TYPE"),
        # "academicLoad": ge_(),
        "deliveryMode": ge_(),
        "planAccreditation": ge_(),
        "subjectBenchmark": ge_(),
        "educationalAimsIntro": ge_(),
        "educationalAims": ge_(),
        "outlineDescription": ge_(),
        "distinguishingFeatures": ge_(),
        "furtherInformation": ge_(),
        "planRequirements": ge_(),
        "includingSubjects": ge_(),
        "excludingSubjects": ge_(),
        "otherRequirements": ge_(),
        "ieltsRequirements": ge_(),
        "generalInformation": ge_(),
        "modules": modules,
        "assessment": ge_(),
        "assessmentMarking": ge_(),
        "progressionInformation": ge_(),
        "borderlineCriteria": ge_(),
        "degreeInformation": ge_(),
        "courseWeightings": ge_(),
        "degreeCalculationModel": ge_(),
        "otherRegulations": ge_(),
        "notwithstandingRegulations": ge_(),
        "overview": ge_(),
        "assessmentMethods": ge_(),
        "teachingAndLearning": ge_(),
        "learningOutcomes": ge_()
}
 
    }
    # pprint(modules)


    # https://github.com/EricWay1024/uCourse-crawler/blob/master/plan.js



get_plan(
    'C6UMTHENM',
    '2024',
    'C',
)