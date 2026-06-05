from pathlib import Path
from datetime import datetime
import json

DATA_FILE = Path(__file__).parent / "activities.json"

def save_activities(activities):
    with open(DATA_FILE, "w") as file:
        json.dump(activities, file, indent=4)

def load_activities():
    try:
        with open(DATA_FILE, "r") as file:
            activities = json.load(file)
        return activities
    except FileNotFoundError:
        return []

activities = load_activities()

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

def add_activity(activities):
    print("Add activity selected")
    category = input(f"Enter category: ").strip()
    task = input(f"Enter Task: ").strip()
    duration = get_positive_float("Enter how many hours you committed to this task: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    activity_data = {
        "task_name" : task,
        "duration" : duration,
        "category" : category,
        "timestamp" : timestamp
    }
    activities.append(activity_data)
    save_activities(activities)

def see_activities(activities):
    print("View activities selected")
    if not activities:
        print("No activities recorded yet.")
    else:
        for i, activity in enumerate(activities):
            print(
                f"- Task {i + 1}: "
                f"Category: {activity['category']} | "
                f"{activity['task_name']} | "
                f"{activity['duration']} hours | "
                f"{activity.get('timestamp', 'No timestamp')}"
            )

def show_total_time(activities):
    print("Show total time selected")
    if not activities:
        print("No activities recorded.")
    else:
        total_time = sum(activity['duration'] for activity in activities)
        print(f"Total time committed: {total_time:.2f} hours")

def show_time_by_category(activities):
    if not activities:
        print("No activities recorded.")
    else:
        category_totals = {}

        for activity in activities:
            duration = activity["duration"]
            category = activity["category"]

            if category not in category_totals:
                category_totals[category] = 0

            category_totals[category] += duration

        for category, total_duration in category_totals.items():
            print(f"{category}: Total Duration: {total_duration:.2f} hours")


def edit_activity(activities):
    if not activities:
        print("No activities recorded")
        return 

    for i, activity in enumerate(activities):
        print(f"- Task {i + 1}: {activity['category']} - {activity['task_name']} {activity['duration']} hours")

    try:
        choice = int(input("Enter the task number to edit: "))
        index = choice - 1

        if index < 0 or index >= len(activities):
            print("Invalid task number.")
            return

        activity = activities[index]

        print(f"Editing: {activity['task_name']}")

        new_category = input("Enter new category: ").strip()
        new_task = input("Enter new task: ").strip()
        new_duration = get_positive_float("Enter new duration in hours: ")

        activity["category"] = new_category
        activity["task_name"] = new_task
        activity["duration"] = new_duration

        save_activities(activities)
        print("Activity updated.")

    except ValueError:
        print("Please enter a valid number.")

def delete_activity(activities):
    if not activities:
        print("No activities recorded.")
        return
    
    for i, activity in enumerate(activities):
        print(f"- Task {i + 1}: {activity['category']} - {activity['task_name']} ({activity['duration']} hours) ")

    try:
        choice =  int(input("Enter the task number to delete: "))
        index = choice - 1

        if index < 0 or index >= len(activities):
            print("Invalid task number.")
            return

        deleted_activity = activities.pop(index)
        save_activities(activities)

        print(f"Deleted: {deleted_activity['task_name']}")
    
    except ValueError:
        print("Please enter a valid number.")


while True:
    print("\nActivity Tracker")
    print("1. Add activity")
    print("2. View activities")
    print("3. Show total time")
    print("4. Show total time by category")
    print("5. Delete activity")
    print("6. Edit activity")
    print("7. Quit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_activity(activities)

    elif choice == "2":
        see_activities(activities)

    elif choice == "3":
        show_total_time(activities)

    elif choice == "4":
        show_time_by_category(activities)

    elif choice == "5":
        delete_activity(activities)

    elif choice == "6":
        edit_activity(activities)

    elif choice == "7":
        print("Goodbye.")
        break

    else:
        print("Invalid choice. Please select 1, 2, 3, 4, 5 or 6.")


