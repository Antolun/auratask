import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "tasks.json")

class Database:
    def __init__(self):
        self._ensure_data_dir()
        self.data = self.load_data()

    def _ensure_data_dir(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

    def get_default_data(self):
        return {
            "tasks": [],
            "stats": {
                "total_focus_minutes": 0,
                "completed_pomodoros": 0,
                "focus_sessions": [],  # List of {"date": "YYYY-MM-DD", "minutes": X}
                "daily_goal_minutes": 100,
                "pomodoro_work_minutes": 25,
                "pomodoro_break_minutes": 5,
                "pomodoro_long_break_minutes": 15
            }
        }

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            data = self.get_default_data()
            self.save_data(data)
            return data
        
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure structure is valid
                if "tasks" not in data:
                    data["tasks"] = []
                if "stats" not in data:
                    data["stats"] = self.get_default_data()["stats"]
                if "daily_goal_minutes" not in data["stats"]:
                    data["stats"]["daily_goal_minutes"] = 100
                if "pomodoro_work_minutes" not in data["stats"]:
                    data["stats"]["pomodoro_work_minutes"] = 25
                if "pomodoro_break_minutes" not in data["stats"]:
                    data["stats"]["pomodoro_break_minutes"] = 5
                if "pomodoro_long_break_minutes" not in data["stats"]:
                    data["stats"]["pomodoro_long_break_minutes"] = 15
                return data

        except Exception as e:
            print(f"Error loading data: {e}. Resetting to default.")
            return self.get_default_data()

    def save_data(self, data=None):
        if data is not None:
            self.data = data
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    # Task operations
    def get_tasks(self):
        return self.data.get("tasks", [])

    def add_task(self, title, description, priority="medium", tags=None, due_date=""):
        if tags is None:
            tags = []
        task_id = str(int(datetime.now().timestamp() * 1000))
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "priority": priority, # "low", "medium", "high"
            "status": "todo", # "todo", "doing", "done"
            "tags": tags,
            "due_date": due_date,
            "focus_time": 0,
            "subtasks": [], # List of {"title": "...", "done": False}
            "created_at": datetime.now().isoformat()
        }
        self.data["tasks"].append(task)
        self.save_data()
        return task

    def update_task_status(self, task_id, new_status):
        for task in self.data["tasks"]:
            if task["id"] == task_id:
                task["status"] = new_status
                self.save_data()
                return True
        return False

    def edit_task(self, task_id, title, description, priority, tags, due_date="", subtasks=None):
        for task in self.data["tasks"]:
            if task["id"] == task_id:
                task["title"] = title
                task["description"] = description
                task["priority"] = priority
                task["tags"] = tags
                task["due_date"] = due_date
                if subtasks is not None:
                    task["subtasks"] = subtasks
                self.save_data()
                return True
        return False

    def update_subtask_state(self, task_id, subtask_idx, is_done):
        for task in self.data["tasks"]:
            if task["id"] == task_id:
                if "subtasks" in task and subtask_idx < len(task["subtasks"]):
                    task["subtasks"][subtask_idx]["done"] = is_done
                    self.save_data()
                    return True
        return False

    def set_daily_goal(self, minutes):
        stats = self.data["stats"]
        stats["daily_goal_minutes"] = minutes
        self.save_data()

    def set_total_focus_time(self, minutes):
        stats = self.data["stats"]
        stats["total_focus_minutes"] = minutes
        self.save_data()

    def set_today_focus_time(self, minutes):
        stats = self.data["stats"]
        from datetime import datetime as _datetime
        today = _datetime.now().strftime("%Y-%m-%d")
        
        old_today_mins = 0
        session_found = False
        for session in stats.get("focus_sessions", []):
            if session["date"] == today:
                old_today_mins = session["minutes"]
                session["minutes"] = minutes
                session_found = True
                break
                
        if not session_found:
            if "focus_sessions" not in stats:
                stats["focus_sessions"] = []
            stats["focus_sessions"].append({
                "date": today,
                "minutes": minutes
            })
            
        diff = minutes - old_today_mins
        stats["total_focus_minutes"] = max(0, stats.get("total_focus_minutes", 0) + diff)
        self.save_data()

    def set_pomodoro_settings(self, work, break_val, long_break):
        stats = self.data["stats"]
        stats["pomodoro_work_minutes"] = work
        stats["pomodoro_break_minutes"] = break_val
        stats["pomodoro_long_break_minutes"] = long_break
        self.save_data()


    def delete_task(self, task_id):
        initial_count = len(self.data["tasks"])
        self.data["tasks"] = [t for t in self.data["tasks"] if t["id"] != task_id]
        if len(self.data["tasks"]) != initial_count:
            self.save_data()
            return True
        return False

    # Stats operations
    def add_focus_time(self, minutes, task_id=None):
        stats = self.data["stats"]
        stats["total_focus_minutes"] += minutes
        stats["completed_pomodoros"] += 1
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Update or add to daily sessions
        session_found = False
        for session in stats["focus_sessions"]:
            if session["date"] == today:
                session["minutes"] += minutes
                session_found = True
                break
        
        if not session_found:
            stats["focus_sessions"].append({
                "date": today,
                "minutes": minutes
            })
            
        # If task_id is provided, associate focus time with that task
        if task_id:
            for task in self.data["tasks"]:
                if task["id"] == task_id:
                    task["focus_time"] = task.get("focus_time", 0) + minutes
                    break
            
        self.save_data()

    def get_stats(self):
        return self.data.get("stats", self.get_default_data()["stats"])
