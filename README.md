
# Task Scheduler with SQLite

This project demonstrates how to create a simple task scheduler using Python and SQLite. The script creates a database with two tables: one for storing tasks and another for logging task executions. Tasks are scheduled to run after a specified interval and are marked as 'completed' once executed.

## Steps:
1. **Database Initialization**: 
   - The script checks if the `tasks` and `logs` tables exist in the SQLite database. 
   - If they don't, the tables are created.

2. **Insert a Task**:
   - A sample task is added to the `tasks` table with an interval of 10 seconds.

3. **Task Scheduling and Execution**:
   - The script queries for all pending tasks (`status = 'pending'`).
   - Each task waits for the specified interval (e.g., 10 seconds), then executes.
   - After execution, the task's status is updated to 'completed' and logged into the `logs` table.

4. **Script Behavior**:
   - The script runs once to execute the task and then stops.
   - To make the script run indefinitely, you can wrap the task scheduling function inside a `while True` loop.

## Code Explanation:

### Database Initialization:
The following code creates the two tables if they don't exist:

```python
with sqlite3.connect('example.db') as connection:
    cursor = connection.cursor()
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        interval_seconds INTEGER NOT NULL,
        status TEXT DEFAULT 'pending'
    )
    ''')
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
```

### Inserting a Sample Task:

```python
with sqlite3.connect('example.db') as connection:
    cursor = connection.cursor()
    cursor.execute(''' 
    INSERT INTO tasks (task_name, interval_seconds) VALUES (?, ?) 
    ''', ("Sample Task", 10))
```

### Task Scheduling and Execution:

```python
def schedule_tasks():
    with sqlite3.connect('example.db') as connection:
        cursor = connection.cursor()
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
```

## To Run the Script:

1. Install Python 3.x.
2. Install the `sqlite3` library (it's included with Python by default).
3. Save the code in a `.py` file.
4. Run the script in a terminal:
   ```bash
   python task_scheduler.py
   ```

## Customizing:
- You can adjust the `interval_seconds` in the task insert statement to set different intervals for your tasks.
- If you want the script to run indefinitely, wrap the `schedule_tasks()` function in a `while True:` loop.

## License:
This project is open source and available under the MIT license.

