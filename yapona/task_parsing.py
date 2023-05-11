from dotenv import load_dotenv
import os
from datetime import datetime

def parse_task_list(path):
    pass

def get_tasks_for_today():
    load_dotenv()
    tasks_dir = os.getenv("TASKS_PATH")
    if tasks_dir is None:
        print("TASKS_PATH not set")
        return None
    today = datetime.today()
    today = today.strftime("%d-%m-%Y")
    today = f"{today}.md"
    today_tasks_path = os.path.join(tasks_dir, today)
    if not os.path.exists(today_tasks_path):
        print(f"{today_tasks_path} does not exist")
        return None
    return today_tasks_path



if __name__ == "__main__":
    task_path = get_tasks_for_today()
    print(task_path)

