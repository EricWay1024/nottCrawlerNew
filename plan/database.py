import sqlite3
import json
from .config import DB_PATH

# SQL Script to create the table
make_table_script = """
CREATE TABLE IF NOT EXISTS plan (
    title TEXT,
    degree TEXT,
    degreeType TEXT,
    year TEXT,
    campus TEXT,
    academicPlanCode TEXT,
    ucasCode TEXT,
    school TEXT,
    planType TEXT,
    deliveryMode TEXT,
    duration TEXT,
    subjectBenchmark TEXT,
    planAccreditation TEXT,
    educationalAimsIntro TEXT,
    educationalAims TEXT,
    outlineDescription TEXT,
    distinguishingFeatures TEXT,
    planRequirements TEXT,
    includingSubjects TEXT,
    excludingSubjects TEXT,
    otherRequirements TEXT,
    ieltsRequirements TEXT,
    generalInformation TEXT,
    assessment TEXT,
    assessmentMarking TEXT,
    progressionInformation TEXT,
    borderlineCriteria TEXT,
    degreeInformation TEXT,
    courseWeightings TEXT,
    degreeCalculationModel TEXT,
    otherRegulations TEXT,
    overview TEXT,
    assessmentMethods TEXT,
    teachingAndLearning TEXT,
    learningOutcomes TEXT,
    modules TEXT,  -- Store modules as JSON string
    PRIMARY KEY (year, campus, academicPlanCode)
);
"""


# Function to check if a plan already exists in the database
def plan_exists(cursor, year, campus, academicPlanCode):
    query = "SELECT 1 FROM plans WHERE year = ? AND campus = ? AND academicPlanCode = ?"
    cursor.execute(query, (year, campus, academicPlanCode))
    return cursor.fetchone() is not None


def insert_plan(cursor, plan_data):
    # Prepare the insert query
    insert_query = '''
    INSERT INTO plans (
        title, 
        degree,
        degreeType,
        year, 
        campus, 
        academicPlanCode, 
        ucasCode, 
        school, 
        planType, 
        deliveryMode, 
        duration, 
        subjectBenchmark, 
        planAccreditation, 
        educationalAimsIntro, 
        educationalAims, 
        outlineDescription, 
        distinguishingFeatures, 
        planRequirements, 
        includingSubjects, 
        excludingSubjects, 
        otherRequirements, 
        ieltsRequirements, 
        generalInformation, 
        assessment, 
        assessmentMarking, 
        progressionInformation, 
        borderlineCriteria, 
        degreeInformation, 
        courseWeightings, 
        degreeCalculationModel, 
        otherRegulations, 
        overview, 
        assessmentMethods, 
        teachingAndLearning, 
        learningOutcomes, 
        modules
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # Insert the plan data into the database
    cursor.execute(insert_query, (
        plan_data["title"], 
        plan_data["degree"],
        plan_data["degreeType"],
        plan_data["year"], plan_data["campus"], plan_data["academicPlanCode"],
        plan_data["ucasCode"], plan_data["school"], plan_data["planType"], plan_data["deliveryMode"],
        plan_data["duration"], plan_data["subjectBenchmark"], plan_data["planAccreditation"],
        plan_data["educationalAimsIntro"], plan_data["educationalAims"], plan_data["outlineDescription"],
        plan_data["distinguishingFeatures"], plan_data["planRequirements"], plan_data["includingSubjects"],
        plan_data["excludingSubjects"], plan_data["otherRequirements"], plan_data["ieltsRequirements"],
        plan_data["generalInformation"], plan_data["assessment"], plan_data["assessmentMarking"],
        plan_data["progressionInformation"], plan_data["borderlineCriteria"], plan_data["degreeInformation"],
        plan_data["courseWeightings"], plan_data["degreeCalculationModel"], plan_data["otherRegulations"],
        plan_data["overview"], plan_data["assessmentMethods"], plan_data["teachingAndLearning"],
        plan_data["learningOutcomes"], json.dumps(plan_data["modules"])
    ))


# Create the SQLite table
def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(make_table_script)
    conn.commit()
    conn.close()

