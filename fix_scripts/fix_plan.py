import sqlite3
from plan.util import get_degree_info

# Database path (adjust this if necessary)
DB_PATH = "./res/data.db"


# Step 1: Add new columns `degree` and `degreeType` to the `plan` table
def add_columns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Adding the new columns
    try:
        cursor.execute("ALTER TABLE plan ADD COLUMN degree TEXT")
        cursor.execute("ALTER TABLE plan ADD COLUMN degreeType TEXT")
    except sqlite3.OperationalError as e:
        print(f"Error occurred while adding columns: {e}")
        # If columns already exist, you can catch and continue

    conn.commit()
    conn.close()


# Step 2: Update existing rows with `degree` and `degreeType` information
def update_plans_with_degree_info():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all rows from the plan table (fetching `title`, which is needed for get_degree_info)
    cursor.execute("SELECT title, year, campus, academicPlanCode FROM plan")
    plans = cursor.fetchall()

    for plan in plans:
        title, year, campus, academicPlanCode = plan

        # Fetch degree information using the `get_degree_info` function
        degree_info = get_degree_info(title)
        degree = degree_info["degree"]
        degree_type = degree_info["degreeType"]

        # Update the row with the degree and degreeType info
        cursor.execute(
            """
            UPDATE plan
            SET degree = ?, degreeType = ?
            WHERE year = ? AND campus = ? AND academicPlanCode = ?
        """,
            (degree, degree_type, year, campus, academicPlanCode),
        )

    conn.commit()
    conn.close()


def main():
    # Step 1: Alter the table to add the new columns
    add_columns()

    # Step 2: Update the existing data with degree and degreeType
    update_plans_with_degree_info()

    print("Database updated successfully.")


if __name__ == "__main__":
    main()
