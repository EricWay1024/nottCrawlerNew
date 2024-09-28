import requests
import urllib.parse


cookies = {
    'AMCV_6F5A143A5F3664160A495FE7%40AdobeOrg': '179643557%7CMCIDTS%7C19738%7CMCMID%7C86764993773768519264838785398543367376%7CMCAID%7CNONE%7CMCOPTOUT-1705324788s%7CNONE%7CvVersion%7C5.5.0',
    '_ga_NTJWP5TDWB': 'GS1.1.1697575947.1.1.1697575970.37.0.0',
    '_ga': 'GA1.1.788458860.1697575947',
    'amp_045277': 'Vfkh_4u7-qLy6ej--rlSa3...1hd1eia0g.1hd1eia0g.0.0.0',
    'PS_DEVICEFEATURES': 'width:1536 height:864 pixelratio:1.25 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0',
    'X-OCI-CSPRD-LBS-Route': '10ec4fd320d3d1a398fb92f3ec907cb602017e5d',
    'gb3cuonpr92web09-8000-PORTAL-PSJSESSIONID': 'Jys4ouRswQ0NhpZQ8SSXUDhJF0rSWBo4!-245173727',
    'ExpirePage': 'https://campus.nottingham.ac.uk/psp/csprd_pub/',
    'PS_LOGINLIST': 'https://campus.nottingham.ac.uk/csprd_pub',
    'PS_TOKENEXPIRE': '28_Sep_2024_12:46:53_GMT',
    'PS_TOKEN': 'pwAAAAQDAgEBAAAAvAIAAAAAAAAsAAAABABTaGRyAk4Abwg4AC4AMQAwABQm4hx/STg0wGpEzTBJx0Ljg1340WcAAAAFAFNkYXRhW3icHYpLDkAwAESfTyws3UNDaaJbZSFEhHTtCC7ocCZm8SbzMg+QZ2mSqN+UP1Vk5+YgMrKxECgiKzNl4JI/megtDZaeWu1FyyC2WgYnY+h+enkn7/TlA5x5C9g=',
    'PS_TokenSite': 'https://campus.nottingham.ac.uk/psc/csprd_pub/?gb3cuonpr92web09-8000-PORTAL-PSJSESSIONID',
    'SignOnDefault': '',
    'PS_LASTSITE': 'https://campus.nottingham.ac.uk/psp/csprd_pub/',
    'ps_theme': 'node:SA portal:EMPLOYEE theme_id:UN_DEFAULT_THEME_FLUID css:UN_BRAND_CLASSIC_TEMPLATE_860 css_f:UN_BRAND_FLUID_TEMPLATE_860 accessibility:N macroset:UN_DEFAULT_MACROSET_860 formfactor:3 piamode:2',
    'psback': '%22%22url%22%3A%22https%3A%2F%2Fcampus.nottingham.ac.uk%2Fpsc%2Fcsprd_pub%2FEMPLOYEE%2FHRMS%2Fc%2FUN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL%3Fpage%3DUN_CRS_EXT2_FPG%22%20%22label%22%3A%22Curriculum%20Catalogue%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fcampus.nottingham.ac.uk%2Fpsc%2Fcsprd_pub%2FEMPLOYEE%2FHRMS%22%22',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://campus.nottingham.ac.uk',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PAGE=UN_CRS_EXT2_FPG&CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS&LINKA=&CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS',
    # 'Cookie': 'AMCV_6F5A143A5F3664160A495FE7%40AdobeOrg=179643557%7CMCIDTS%7C19738%7CMCMID%7C86764993773768519264838785398543367376%7CMCAID%7CNONE%7CMCOPTOUT-1705324788s%7CNONE%7CvVersion%7C5.5.0; _ga_NTJWP5TDWB=GS1.1.1697575947.1.1.1697575970.37.0.0; _ga=GA1.1.788458860.1697575947; amp_045277=Vfkh_4u7-qLy6ej--rlSa3...1hd1eia0g.1hd1eia0g.0.0.0; PS_DEVICEFEATURES=width:1536 height:864 pixelratio:1.25 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; X-OCI-CSPRD-LBS-Route=10ec4fd320d3d1a398fb92f3ec907cb602017e5d; gb3cuonpr92web09-8000-PORTAL-PSJSESSIONID=Jys4ouRswQ0NhpZQ8SSXUDhJF0rSWBo4!-245173727; ExpirePage=https://campus.nottingham.ac.uk/psp/csprd_pub/; PS_LOGINLIST=https://campus.nottingham.ac.uk/csprd_pub; PS_TOKENEXPIRE=28_Sep_2024_12:46:53_GMT; PS_TOKEN=pwAAAAQDAgEBAAAAvAIAAAAAAAAsAAAABABTaGRyAk4Abwg4AC4AMQAwABQm4hx/STg0wGpEzTBJx0Ljg1340WcAAAAFAFNkYXRhW3icHYpLDkAwAESfTyws3UNDaaJbZSFEhHTtCC7ocCZm8SbzMg+QZ2mSqN+UP1Vk5+YgMrKxECgiKzNl4JI/megtDZaeWu1FyyC2WgYnY+h+enkn7/TlA5x5C9g=; PS_TokenSite=https://campus.nottingham.ac.uk/psc/csprd_pub/?gb3cuonpr92web09-8000-PORTAL-PSJSESSIONID; SignOnDefault=; PS_LASTSITE=https://campus.nottingham.ac.uk/psp/csprd_pub/; ps_theme=node:SA portal:EMPLOYEE theme_id:UN_DEFAULT_THEME_FLUID css:UN_BRAND_CLASSIC_TEMPLATE_860 css_f:UN_BRAND_FLUID_TEMPLATE_860 accessibility:N macroset:UN_DEFAULT_MACROSET_860 formfactor:3 piamode:2; psback=%22%22url%22%3A%22https%3A%2F%2Fcampus.nottingham.ac.uk%2Fpsc%2Fcsprd_pub%2FEMPLOYEE%2FHRMS%2Fc%2FUN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL%3Fpage%3DUN_CRS_EXT2_FPG%22%20%22label%22%3A%22Curriculum%20Catalogue%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fcampus.nottingham.ac.uk%2Fpsc%2Fcsprd_pub%2FEMPLOYEE%2FHRMS%22%22',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'Priority': 'u=0',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

state_num = 60
address_link = 9
school_code = 'UDD-ACS'

data = urllib.parse.urlencode({
    "ICAJAX": "1",
    "ICNAVTYPEDROPDOWN": "0",
    "ICType": "Panel",
    "ICElementNum": "0",
    "ICStateNum": f"{state_num}",
    "ICAction": f"ADDRESS_LINK${address_link}",
    "ICModelCancel": "0",
    "ICXPos": "0",
    "ICYPos": "0",
    "ResponsetoDiffFrame": "-1",
    "TargetFrameName": "None",
    "FacetPath": "None",
    "ICFocus": "",
    "ICSaveWarningFilter": "0",
    "ICChanged": "0",
    "ICSkipPending": "0",
    "ICAutoSave": "0",
    "ICResubmit": "0",
    "ICSID": "9ef/zHqKqj9d2VSoH7gqjMO1n0V3WN1HLDmaQ6cU5FQ=",
    "ICActionPrompt": "false",
    "ICTypeAheadID": "",
    "ICBcDomData": f"""*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=Immigration%20and%20Ethnicity%20in%20the%20United%20States&MODULE=AMCS2007&CRSEID=011262&LINKA=&LINKB=&LINKC=UDD-ACS&~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_MODULE_SEARCH_F~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PortalKeyStruct=yes~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_PLN_EXT1_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=From%20Landscapes%20to%20Mixtapes:%20Canadian%20Literature,%20Film%20and%20Culture&MODULE=AMCS1008&CRSEID=011286&LINKA=&LINKB=&LINKC=UDD-ACS~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=Immigration%20and%20Ethnicity%20in%20the%20United%20States&MODULE=AMCS2007&CRSEID=011262&LINKA=&LINKB=&LINKC=UDD-ACS~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=Immigration%20and%20Ethnicity%20in%20the%20United%20States&MODULE=AMCS2007&CRSEID=011262&LINKA=&LINKB=&LINKC=UDD-ACS~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=Immigration%20and%20Ethnicity%20in%20the%20United%20States&MODULE=AMCS2007&CRSEID=011262&LINKA=&LINKB=&LINKC=UDD-ACS~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=From%20Landscapes%20to%20Mixtapes:%20Canadian%20Literature,%20Film%20and%20Culture&MODULE=AMCS1008&CRSEID=011286&LINKA=&LINKB=&LINKC=UDD-ACS~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=Popular%20Music%20Cultures%20&%20Countercultures%20(PGT%2020)&MODULE=AMCS4070&CRSEID=031971&LINKA=&LINKB=&LINKC=UDD-ACS~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=Immigration%20and%20Ethnicity%20in%20the%20United%20States&MODULE=AMCS2007&CRSEID=011262&LINKA=&LINKB=&LINKC=UDD-ACS~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=Dissertation%20in%20American%20and%20Canadian%20Studies&MODULE=AMCS3004&CRSEID=008334&LINKA=&LINKB=&LINKC=UDD-ACS~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=Sexuality%20in%20American%20History%20(Level%203)&MODULE=AMCS3061&CRSEID=022814&LINKA=&LINKB=&LINKC=UDD-ACS~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=North%20American%20Regions&MODULE=AMCS2054&CRSEID=022802&LINKA=&LINKB=&LINKC=UDD-ACS~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-ACS&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_PLN_EXT1_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=UDD-PSGY&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_PLN_EXT1_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=USC-MATH&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=Mathematical%20Methods%20for%20Architectural%20and%20Environmental%20Engineering&MODULE=MTHS1007&CRSEID=032386&LINKA=&LINKB=&LINKC=USC-MATH~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=USC-MATH&LINKA=~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT4_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=Gravity,%20Particles%20and%20Fields%20Dissertation&MODULE=MATH4050&CRSEID=014538&LINKA=&LINKB=&LINKC=USC-MATH~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_PLN_EXT1_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module~UnknownValue*C~UnknownValue~EMPLOYEE~HRMS~UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL~UN_CRS_EXT2_FPG~Curriculum Catalogue~UnknownValue~UnknownValue~https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL={school_code}&LINKA=~UnknownValue""",
    "ICDNDSrc": "",
    "ICPanelHelpUrl": "",
    "ICPanelName": "",
    "ICPanelControlStyle": "pst_side2-hidden pst_panel-mode ",
    "ICFind": "",
    "ICAddCount": "",
    "ICAppClsData": "",
    "win0hdrdivPT_SYSACT_RETLST": "psc_hidden",
    "win0hdrdivPT_SYSACT_HELP": "psc_hidden"
})

response = requests.post(
    'https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL',
    cookies=cookies,
    headers=headers,
    data=data,
)


print(response.text)
