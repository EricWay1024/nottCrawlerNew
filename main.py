import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from retry import retry

# cookies = {
#     'AMCV_6F5A143A5F3664160A495FE7%40AdobeOrg': '179643557%7CMCIDTS%7C19738%7CMCMID%7C86764993773768519264838785398543367376%7CMCAID%7CNONE%7CMCOPTOUT-1705324788s%7CNONE%7CvVersion%7C5.5.0',
#     '_ga_NTJWP5TDWB': 'GS1.1.1697575947.1.1.1697575970.37.0.0',
#     '_ga': 'GA1.1.788458860.1697575947',
#     'amp_045277': 'Vfkh_4u7-qLy6ej--rlSa3...1hd1eia0g.1hd1eia0g.0.0.0',
#     'PS_DEVICEFEATURES': 'width:1536 height:864 pixelratio:1.25 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0',
#     'X-OCI-CSPRD-LBS-Route': '10ec4fd320d3d1a398fb92f3ec907cb602017e5d',
#     'gb3cuonpr92web09-8000-PORTAL-PSJSESSIONID': 'bVo3229mHGRvSgt-FSIxZNWRtSQqF2N4!-245173727',
#     'ExpirePage': 'https://campus.nottingham.ac.uk/psp/csprd_pub/',
#     'PS_LOGINLIST': 'https://campus.nottingham.ac.uk/csprd_pub',
#     'PS_TOKENEXPIRE': '28_Sep_2024_09:06:57_GMT',
#     'PS_TOKEN': 'pwAAAAQDAgEBAAAAvAIAAAAAAAAsAAAABABTaGRyAk4Abwg4AC4AMQAwABQm4hx/STg0wGpEzTBJx0Ljg1340WcAAAAFAFNkYXRhW3icHYpLDkAwAESfTyws3UNDaaJbZSFEhHTtCC7ocCZm8SbzMg+QZ2mSqN+UP1Vk5+YgMrKxECgiKzNl4JI/megtDZaeWu1FyyC2WgYnY+h+enkn7/TlA5x5C9g=',
#     'PS_TokenSite': 'https://campus.nottingham.ac.uk/psc/csprd_pub/?gb3cuonpr92web09-8000-PORTAL-PSJSESSIONID',
#     'SignOnDefault': '',
#     'PS_LASTSITE': 'https://campus.nottingham.ac.uk/psp/csprd_pub/',
#     'ps_theme': 'node:SA portal:EMPLOYEE theme_id:UN_DEFAULT_THEME_FLUID css:UN_BRAND_CLASSIC_TEMPLATE_860 css_f:UN_BRAND_FLUID_TEMPLATE_860 accessibility:N macroset:UN_DEFAULT_MACROSET_860 formfactor:3 piamode:2',
#     'psback': '%22%22url%22%3A%22https%3A%2F%2Fcampus.nottingham.ac.uk%2Fpsc%2Fcsprd_pub%2FEMPLOYEE%2FHRMS%2Fc%2FUN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL%3Fpage%3DUN_PLN_EXT1_FPG%22%20%22label%22%3A%22Curriculum%20Catalogue%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fcampus.nottingham.ac.uk%2Fpsc%2Fcsprd_pub%2FEMPLOYEE%2FHRMS%22%22',
# }

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
#     'Accept-Language': 'en-US,en;q=0.5',
#     # 'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Referer': 'https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PortalActualURL=https%3a%2f%2fcampus.nottingham.ac.uk%2fpsc%2fcsprd_pub%2fEMPLOYEE%2fHRMS%2fc%2fUN_PROG_AND_MOD_EXTRACT.UN_PAM_CRSE_EXTRCT.GBL&PortalContentURL=https%3a%2f%2fcampus.nottingham.ac.uk%2fpsc%2fcsprd_pub%2fEMPLOYEE%2fHRMS%2fc%2fUN_PROG_AND_MOD_EXTRACT.UN_PAM_CRSE_EXTRCT.GBL&PortalContentProvider=HRMS&PortalCRefLabel=Course%20Extract&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fcampus.nottingham.ac.uk%2fpsp%2fcsprd_pub%2f&PortalURI=https%3a%2f%2fcampus.nottingham.ac.uk%2fpsc%2fcsprd_pub%2f&PortalHostNode=SA&NoCrumbs=yes&PortalKeyStruct=yes',
#     'DNT': '1',
#     'Connection': 'keep-alive',
#     # 'Cookie': 'AMCV_6F5A143A5F3664160A495FE7%40AdobeOrg=179643557%7CMCIDTS%7C19738%7CMCMID%7C86764993773768519264838785398543367376%7CMCAID%7CNONE%7CMCOPTOUT-1705324788s%7CNONE%7CvVersion%7C5.5.0; _ga_NTJWP5TDWB=GS1.1.1697575947.1.1.1697575970.37.0.0; _ga=GA1.1.788458860.1697575947; amp_045277=Vfkh_4u7-qLy6ej--rlSa3...1hd1eia0g.1hd1eia0g.0.0.0; PS_DEVICEFEATURES=width:1536 height:864 pixelratio:1.25 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; X-OCI-CSPRD-LBS-Route=10ec4fd320d3d1a398fb92f3ec907cb602017e5d; gb3cuonpr92web09-8000-PORTAL-PSJSESSIONID=bVo3229mHGRvSgt-FSIxZNWRtSQqF2N4!-245173727; ExpirePage=https://campus.nottingham.ac.uk/psp/csprd_pub/; PS_LOGINLIST=https://campus.nottingham.ac.uk/csprd_pub; PS_TOKENEXPIRE=28_Sep_2024_09:06:57_GMT; PS_TOKEN=pwAAAAQDAgEBAAAAvAIAAAAAAAAsAAAABABTaGRyAk4Abwg4AC4AMQAwABQm4hx/STg0wGpEzTBJx0Ljg1340WcAAAAFAFNkYXRhW3icHYpLDkAwAESfTyws3UNDaaJbZSFEhHTtCC7ocCZm8SbzMg+QZ2mSqN+UP1Vk5+YgMrKxECgiKzNl4JI/megtDZaeWu1FyyC2WgYnY+h+enkn7/TlA5x5C9g=; PS_TokenSite=https://campus.nottingham.ac.uk/psc/csprd_pub/?gb3cuonpr92web09-8000-PORTAL-PSJSESSIONID; SignOnDefault=; PS_LASTSITE=https://campus.nottingham.ac.uk/psp/csprd_pub/; ps_theme=node:SA portal:EMPLOYEE theme_id:UN_DEFAULT_THEME_FLUID css:UN_BRAND_CLASSIC_TEMPLATE_860 css_f:UN_BRAND_FLUID_TEMPLATE_860 accessibility:N macroset:UN_DEFAULT_MACROSET_860 formfactor:3 piamode:2; psback=%22%22url%22%3A%22https%3A%2F%2Fcampus.nottingham.ac.uk%2Fpsc%2Fcsprd_pub%2FEMPLOYEE%2FHRMS%2Fc%2FUN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL%3Fpage%3DUN_PLN_EXT1_FPG%22%20%22label%22%3A%22Curriculum%20Catalogue%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fcampus.nottingham.ac.uk%2Fpsc%2Fcsprd_pub%2FEMPLOYEE%2FHRMS%22%22',
#     'Upgrade-Insecure-Requests': '1',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-User': '?1',
#     'Sec-GPC': '1',
#     'Priority': 'u=0, i',
#     # Requests doesn't support trailers
#     # 'TE': 'trailers',
# }


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
