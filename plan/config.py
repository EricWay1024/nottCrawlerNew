import json

YEAR = "2025"
PLAN_BRIEF_PATH = "./res/plan_brief.json"
DB_PATH = "./res/data.db"
PLAN_TABLE_NAME = "plan"
PLAN_SCHEMA_PATH = "./schemas/plan-schema.json"
PLAN_SCHEMA = json.load(open(PLAN_SCHEMA_PATH))

# This is a list, not a string! Look at the end
DEG_LIST = """Bachelor of Architecture with Honours
Bachelor of Arts with Honours
Bachelor of Arts with Joint Honours
Bachelor of Arts (Ordinary)
Bachelor of Education with Honours
Bachelor of Engineering with Honours
Bachelor of Laws with Honours
Bachelor of Medical Sciences with Honours
Bachelor of Medicine and Bachelor of Surgery
Bachelor of Pharmacy with Honours
Bachelor of Science (Ordinary)
Bachelor of Science with Honours
Bachelor of Science with Joint Honours
Bachelor of Vet Med and Bachelor of Vet Surgery
Bachelor of Veterinary Medical Sciences with Hons
Certificate (Foundation Year)
Certificate
Doctor of Applied Educational Psychology
Doctor of Clinical Psychology
Doctor of Education Professional
Doctor of Engineering
Doctor of Medicine
Doctor of Philosophy
Doctor of Public Management
Doctor of Public Policy
Doctor of Science
Doctor of Veterinary
Graduate Diploma
Master in Architecture
Master in Engineering with Honours
Master in Mathematics with Honours
Master in Science with Honours
Master of Architecture
Master of Arts
Master of Business
Master of Laws
Master of Medical Sciences
Master of Nursing Science with Honours
Master of Nutrition
Master of Pharmacy with Honours
Master of Philosophy
Master of Public Administration
Master of Public Health
Master of Research
Master of Science
Master of Technology
Master of Veterinary Medicine
Master of Veterinary Surgery
No Qualification
Post Graduate Certificate in Education
Postgraduate Certificate
Postgraduate Diploma
Professional Doctorate in Forensic Psychology""".split(
    "\n"
)
