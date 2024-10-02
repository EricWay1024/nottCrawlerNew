import json

YEAR = "2024"
SCHOOLS_PATH = "./res/schools.json"
MODULE_BRIEF_PATH = "./res/module_brief.json"
DB_PATH = "./res/data.db"
COURSE_TABLE_NAME = "course"
THREADS = (
    9  # Could be more if you have a powerful computer and stable Internet
)
HEADLESS = True  # Set to False for testing
# Define the path to chromedriver.exe
DRIVER_PATH = "C:\\Users\\eric\\apps\\chromedriver.exe"
# For Testing, we only run it for the Malaysia campus
TESTING = True
MODULE_SCHEMA_PATH = "./schemas/module-schema.json"
MODULE_SCHEMA = json.load(open(MODULE_SCHEMA_PATH))
