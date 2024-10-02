# New (as of October 2024) Crawler for University of Nottingham Course Catalogue

[Data source](https://campus.nottingham.ac.uk/psp/csprd_pub/EMPLOYEE/HRMS/c/UN_PROG_AND_MOD_EXTRACT.UN_PAM_CRSE_EXTRCT.GBL).

The catalogue has undergone some big changes this year but it's still far less good than [Nott Course](https://nott-course.uk) so the crawler is here.

I personally prefer Python so I ditched [the old JS crawler](https://github.com/EricWay1024/uCourse-crawler/) and rewrote everything.

To run (you may want a `venv` environment):
```
pip install -r requirements.txt
mkdir res
python -m plan.main
python -m module.fetch_brief
python -m module.fetch_modules
```
Oh, you also need to set up the Chrome webdriver for Selenium... I hope you know how to do it.

Current features:
- Concurrency!!
- Resumable download!!!

Technical notes:
- `plan` only relies on `requests` + `beautifulsoup4`.
- `module` needs `selenium` in addition, because it wasn't clear to me how to obtain a `CRSEID` field in the request. So it's a bit slow.


TODO:

- [x] Refactor the `module` module
- [ ] Make `module` more stable ~~(currently have to run a lot of times)~~ (It seems beter now, but needs further test)
- A blog post on how on developed these
- [x] **Output Data Specification**
- Rewrite this README
- [x] Conform to flake8

The output data format has changed so nott-course also changed a bit.

---

Note: campus should always be a single letter in ['C', 'M', 'U']!!!

Change of course fields:
- Add corequisites
- Add classComment
- courseWebLinks has disappeared (it was useless anyway)
- Add duration to assessments
- In requisites and corequisites, ["code", "title"] has replaced  {"Code": "subject", "Title": "courseTitle"}
- Convenor is now a string (name of the person), not an object


Change of plan fields:
- courseWeightings has become a string, not a table
- degreeCalculationModel has become a string, not a table
- subjectBenchmark HTML
- planAccreditation HTML
- school has become a string too
- the only object field is now modules
- academicLoad has disappeared
- added year and campus
- No furtherInformation
- No notwithstandingRegulations
- add additionalRegulations
- remove "overview"
        "assessmentMethods"
        "teachingAndLearning" => everything in learning outcomes

Finally, a big thanks to... ChatGPT for helping me write this project.