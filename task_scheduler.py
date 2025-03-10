import sqlite3
import time
# test

with sqlite3.connect('example.db') as connection:
    # create tasks table
    with connection:
        cursor = connection.cursor()
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            interval_seconds INTEGER NOT NULL,
            status TEXT DEFAULT 'pending'
        )
        ''')

        # Create logs table
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

    print("Database initialized successfully!")

# insert a task
with sqlite3.connect('example.db') as connection:
    with connection:
        cursor = connection.cursor()
        cursor.execute(''' 
        INSERT INTO tasks (task_name, interval_seconds) VALUES (?, ?) 
        ''', ("Sample Task", 10))

        print("Sample task added!")

def schedule_tasks():
    try:
        with sqlite3.connect('example.db') as connection:
            cursor = connection.cursor()
            # get all pending tasks
            cursor.execute("SELECT * FROM tasks WHERE status = 'pending'")
            tasks = cursor.fetchall()

            for task in tasks:
                task_id, task_name, interval_seconds = task[0], task[1], task[2]
                time.sleep(interval_seconds)

                # update task as complete
                cursor.execute('''
                UPDATE tasks SET status = 'completed' WHERE id = ?
                ''', (task_id,))

                # log the execution
                cursor.execute('''
                INSERT INTO logs (task_name) VALUES (?)
                ''', (task_name,))

                print(f"Task {task_name} executed.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"General error: {e}")

if __name__ == "__main__":
    schedule_tasks()