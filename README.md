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

To run:
```mkdir res```
```python -m plan.main```
```python -m module.fetch_brief```
```python -m module.fetch_modules```

TODO:
- Refactor the `module` module
- Make `module` more stable (currently have to run a lot of times)
- A blog post on how on developed these
- **Output Data Description**