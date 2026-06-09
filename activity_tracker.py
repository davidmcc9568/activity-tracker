from pathlib import Path
from datetime import datetime
import sqlite3

DB_FILE = Path(__file__).parent / "activities.db"

def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT, 
        duration REAL,
        category TEXT,
        timestamp TEXT                   
    )
    """)

    conn.commit()
    conn.close()

create_table()

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

def add_activity():
    print("Add activity selected")
    category = input(f"Enter category: ").strip()
    task = input(f"Enter Task: ").strip()
    duration = get_positive_float("Enter how many hours you committed to this task: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO activities
    (task_name, duration, category, timestamp)
    VALUES (?, ?, ?, ?) 
    """, (task, duration, category, timestamp))


    conn.commit()
    conn.close()

    print("Activity added.")

def see_activities():
    print("View activities selected")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM activities
    ORDER BY id
    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        print("No activities recorded yet.")
        return
    
    for row in rows:
        print(
            "--------------------------------------------------\n"
            f"ID: {row[0]} \n"
            f"Category: {row[3]} \n"
            f"Task: {row[1]} \n"
            f"Duration: {row[2]} hours \n"
            f"Created: {row[4]}\n"
            "--------------------------------------------------\n"
        )

def show_total_time():
    print("Show total time selected")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(duration)
    FROM activities
    """)

    total_time = cursor.fetchone()[0]

    conn.close()

    if total_time is None:
        print("No activities recorded.")
    else:
        print(f"Total time committed: {total_time:.2f} hours")

def show_time_by_category():
    print("Show total time by category selected")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category, SUM(duration)
    FROM activities
    GROUP BY category
    ORDER BY category
    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        print("No activities recorded.")
        return

    for row in rows:
        category = row[0]
        total_duration = row[1]
        print(f"{category}: {total_duration:.2f} hours")

def edit_activity():
    see_activities()

    try:
        activity_id = int(input("Enter the ID of the activity to edit: "))

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM activities
        WHERE id = ?
        """, (activity_id,))

        activity = cursor.fetchone()

        if activity is None:
            print(f"No activity found with ID {activity_id}.")
            conn.close()
            return

        print(
            f"Editing: {activity[1]} | "
            f"{activity[3]} | "
            f"{activity[2]} hours"
        )

        new_category = input("Enter new category: ").strip()
        new_task = input("Enter new task: ").strip()
        new_duration = get_positive_float("Enter new duration in hours: ")

        cursor.execute("""
        UPDATE activities
        SET task_name = ?, duration = ?, category = ?
        WHERE id = ?
        """, (new_task, new_duration, new_category, activity_id))

        conn.commit()
        conn.close()

        print("Activity updated.")

    except ValueError:
        print("Please enter a valid number.")

def delete_activity():
    see_activities()

    try:
        activity_id = int(input("Enter the ID of the activity to delete: "))

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM activities
        WHERE id = ?
        """, (activity_id,))

        activity = cursor.fetchone()

        if activity is None:
            print(f"No activity found with ID {activity_id}.")
            conn.close()
            return

        cursor.execute("""
        DELETE FROM activities
        WHERE id = ?
        """, (activity_id,))

        conn.commit()
        conn.close()

        print(
            f"Deleted: {activity[1]} | "
            f"{activity[3]} | "
            f"{activity[2]} hours"
        )

    except ValueError:
        print("Please enter a valid number.")

while True:
    print(
        """    ========================
        Activity Tracker
    ========================
    1. Add Activity
    2. View Activities
    3. Show total time
    4. Show category summary
    5. Delete activity
    6. Edit activity
    7. Quit"""
    )

    choice = input("Choose an option: ")

    if choice == "1":
        add_activity()

    elif choice == "2":
        see_activities()

    elif choice == "3":
        show_total_time()

    elif choice == "4":
        show_time_by_category()

    elif choice == "5":
        delete_activity()

    elif choice == "6":
        edit_activity()

    elif choice == "7":
        print("Goodbye.")
        break

    else:
        print("Invalid choice. Please select 1, 2, 3, 4, 5, 6, or 7.")


