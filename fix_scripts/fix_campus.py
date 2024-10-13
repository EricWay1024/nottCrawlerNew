import sqlite3

# Database path (adjust this if necessary)
DB_PATH = "./res/data.db"


# Step 1: Update the 'campus' column in the `plan` table to use only the first letter of the current value
def update_plan_campus():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Update the campus field to the first letter of the current campus value
    cursor.execute("UPDATE plan SET campus = SUBSTR(campus, 1, 1)")

    conn.commit()
    conn.close()
    print("Updated 'campus' column in 'plan' table.")


# Step 2: Add the 'campus' column to the `course` table and set it based on the last character of 'mycode'
def update_course_campus():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Step 2.1: Add the new 'campus' column to the `course` table
    try:
        cursor.execute("ALTER TABLE course ADD COLUMN campus TEXT")
    except sqlite3.OperationalError as e:
        # If the column already exists, we just ignore this error
        print(f"Error while adding 'campus' column to 'course' table: {e}")

    # Step 2.2: Update the 'campus' column in `course` table to the last character of the 'mycode' field
    cursor.execute("UPDATE course SET campus = SUBSTR(mycode, -1, 1)")

    conn.commit()
    conn.close()
    print("Updated 'campus' column in 'course' table based on 'mycode'.")


def main():
    # Step 1: Update the campus field in the plan table
    update_plan_campus()

    # Step 2: Add and update the campus field in the course table
    update_course_campus()

    print("Database updates completed successfully.")


if __name__ == "__main__":
    main()
