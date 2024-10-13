# New (as of October 2024) Crawler for University of Nottingham Course Catalogue

Our data source is [the UoN Course Catalogue](https://campus.nottingham.ac.uk/psp/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PAM_CRSE_EXTRCT.GBL).
The catalogue has undergone some big changes this year, but it's still far less good than [Nott Course](https://nott-course.uk) and people are asking me to update the data, so the crawler is here.
I personally prefer Python so I ditched [the old JS crawler](https://github.com/EricWay1024/uCourse-crawler/) and rewrote everything.

## Acknowledgements

A big thanks to... 
- my friend [Lucien](https://github.com/lucienshawls) for helping with the reimagined, Selenium-free `module` crawler (see [issue #1](#1));
- and ChatGPT for making things easier.


## Overview

This crawler has two parts: one for the (course) modules and one for the academic plans and they are written as two (Python) modules, `module` and `plan`.
The `module` module requires Selenium, requests and BeautifulSoup whereas the `plan` module only relies on the latter two.

An overview of the work flow:

- When you run the `module` module, it will first obtain a list of schools of the three campuses and store it in a JSON file. Then it will obtain a list of modules of each school (like the information you see [here](https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PAGE=UN_CRS_EXT2_FPG&CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=USC-MATH&LINKA=&CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=&Module=&SCHOOL=USC-MATH)). Then a POST request (with session information) is sent to fetch the link for the page of each module (see [issue #1](#1) for details), and then a GET request  to fetch the module details (like the information you see [here](https://campus.nottingham.ac.uk/psc/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PLN_EXTRT_FL_CP.GBL?PAGE=UN_CRS_EXT4_FPG&CAMPUS=U&TYPE=Module&YEAR=2024&TITLE=Game%20Theory&MODULE=MATH3004&CRSEID=004662&LINKA=&LINKB=&LINKC=USC-MATH)). We store the data in a SQLite database, where each column is TEXT -- for dictionaries or lists, they are `json.dumps`-ed into a string.
- When you run the `plan` module, it will first obtain a list of academic plans for each campus, and store these pieces of 'plan brief' in a JSON file. Then it will fetch the detail of each plan (not using Selenium this time, so faster), and again store the data in a SQLite database.

Check `schemas` for the JSON schemas of the plan and module objects stored in the SQLite database.

## Features
- Concurrency!!!
- Resumable download!!!

## Get Started!

First you need a `venv` environment which I assume you know how to set up.
Also modify other variables in `module/config.py` and `plan/config.py` if needed.
```
pip install -r requirements.txt
mkdir res
python -m plan.main
python -m module.main
```

If anything went wrong in the process of crawling, you can always just restart the script and it will resume downloading by skipping what has been fetched in the database. Then you should produce a `data.db` file in the `res` directory (if you didn't change the relevant `config` fields), which is used by the [backend server](https://github.com/EricWay1024/nott-course-server-cpp).

<!-- Technical notes:
- `plan` only relies on `requests` + `beautifulsoup4`.
- `module` needs `selenium` in addition, because it wasn't clear to me how to obtain a `CRSEID` field in the request. So it's a bit slow. -->


## To-dos

- [x] Refactor the `module` module
- [x] Make `module` more stable (stable now after removing `selenium` dependency)
- [x] **Output Data Specification**
- [x] Rewrite this README
- [x] Conform to flake8
- [ ] A blog post on how I developed these

The output data format has changed so nott-course also changed a bit.

## Important note

`campus` should always be a single letter in ['C', 'M', 'U'], not the full name!!!

## Change of output fields compared to the [previous crawler](https://github.com/EricWay1024/uCourse-crawler/)

**You don't need to read this section now.**

Change of course fields:
- Add corequisites
- Add classComment
- courseWebLinks has disappeared (it was useless anyway)
- Add duration to assessments
- In requisites and corequisites, ["code", "title"] has replaced "subject", "courseTitle"
- Convenor is now a string (name of the person), not an object


Change of plan fields:
- courseWeightings has become a string, not a table
- degreeCalculationModel has become a string, not a table
- subjectBenchmark HTML
- planAccreditation HTML
- school has become a string too
- the only object field is now modules
- academicLoad has disappeared
- No furtherInformation
- notwithstandingRegulations changing to additionalRegulations
- added year and campus
- remove "overview", "assessmentMethods", "teachingAndLearning" => everything in learning outcomes