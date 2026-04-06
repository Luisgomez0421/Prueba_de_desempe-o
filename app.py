import json
import os

# ---------- GLOBAL VARIABLES ----------
tasks = []
FILE_NAME = "tasks.json"


# ---------- DATA PERSISTENCE ----------
def load_tasks():
    """Load tasks from JSON file"""
    global tasks
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                tasks = json.load(file)
        except (json.JSONDecodeError, IOError):
            # Si el archivo está corrupto o vacío, empezamos con lista vacía
            tasks = []
    else:
        tasks = []


def save_tasks():
    """Save tasks to JSON file"""
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(tasks, file, indent=4)
    except IOError as e:
        print(f"Error saving tasks: {e}")


# ---------- CORE FUNCTIONS ----------
def generate_id():
    """Generate unique ID based on the highest current ID"""
    if not tasks:
        return 1
    # Buscamos el ID más alto de la lista para evitar duplicados al borrar
    max_id = max(task['id'] for task in tasks)
    return max_id + 1


def add_task():
    """Add new task"""
    print("\n--- Add Task ---")
    title = input("Enter title: ")
    description = input("Enter description: ")
    priority = input("Enter priority (high, medium, low): ").lower()

    task = {
        "id": generate_id(),
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending"
    }

    tasks.append(task)
    save_tasks()
    print(f"Task added successfully with ID: {task['id']}")


def show_tasks():
    """Show all tasks"""
    print("\n--- Task List ---")
    if not tasks:
        print("No tasks available.")
        return

    for task in tasks:
        print(f"""
ID: {task['id']}
Title: {task['title']}
Description: {task['description']}
Priority: {task['priority']}
Status: {task['status']}
------------------------""")


def search_task():
    """Search task by ID or title"""
    print("\n--- Search Task ---")
    option = input("Search by (1) ID or (2) Title: ")

    if option == "1":
        try:
            task_id = int(input("Enter ID: "))
            for task in tasks:
                if task["id"] == task_id:
                    print(task)
                    return
            print("Task not found.")
        except ValueError:
            print("Invalid ID. Please enter a number.")

    elif option == "2":
        title = input("Enter title: ").lower()
        found = False
        for task in tasks:
            if title in task["title"].lower():
                print(task)
                found = True
        if not found:
            print("No tasks found.")


def update_task():
    """Update task"""
    print("\n--- Update Task ---")
    try:
        task_id = int(input("Enter task ID: "))
        for task in tasks:
            if task["id"] == task_id:
                task["title"] = input(f"New title ({task['title']}): ") or task['title']
                task["description"] = input(f"New description ({task['description']}): ") or task['description']
                task["priority"] = input(f"New priority ({task['priority']}): ") or task['priority']
                task["status"] = input(f"New status ({task['status']}): ") or task['status']
                save_tasks()
                print("Task updated!")
                return
        print("Task not found.")
    except ValueError:
        print("Invalid input.")


def delete_task():
    """Delete task"""
    print("\n--- Delete Task ---")
    try:
        task_id = int(input("Enter task ID: "))
        for task in tasks:
            if task["id"] == task_id:
                tasks.remove(task)
                save_tasks()
                print("Task deleted!")
                return
        print("Task not found.")
    except ValueError:
        print("Invalid input.")


# ---------- MENU ----------
def show_menu():
    print("""
====== TASK MANAGER ======
1. Add Task
2. Show Tasks
3. Search Task
4. Update Task
5. Delete Task
6. Exit
""")


def main():
    load_tasks()

    option = ""
    while option != "6":
        show_menu()
        option = input("Choose an option: ")

        if option == "1":
            add_task()
        elif option == "2":
            show_tasks()
        elif option == "3":
            search_task()
        elif option == "4":
            update_task()
        elif option == "5":
            delete_task()
        elif option == "6":
            print("Goodbye!")
        else:
            if option != "6":
                print("Invalid option.")


# ---------- RUN PROGRAM ----------
if __name__ == "__main__":
    main()