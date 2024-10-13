import json

YEAR = "2024"
SCHOOLS_PATH = "./res/schools.json"
MODULE_BRIEF_PATH = "./res/module_brief.json"
DB_PATH = "./res/data.db"
COURSE_TABLE_NAME = "course"
# For Testing, we only run it for the Malaysia campus
TESTING = False
MODULE_SCHEMA_PATH = "./schemas/module-schema.json"
MODULE_SCHEMA = json.load(open(MODULE_SCHEMA_PATH))
RETRY_NUM = 6
