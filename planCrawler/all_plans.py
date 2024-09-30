import requests
from bs4 import BeautifulSoup


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

