import os
import shutil
from database import Database

def run_tests():
    print("Testing Database...")
    
    # 1. Initialize DB (will create default file if not exists)
    db = Database()
    print("✓ Database initialized.")
    
    # Check default structure
    assert isinstance(db.get_tasks(), list), "Tasks should be a list"
    assert isinstance(db.get_stats(), dict), "Stats should be a dict"
    print("✓ Default data structures verified.")
    
    # 2. Add Task
    task = db.add_task(
        title="Test Task Title",
        description="Test description details.",
        priority="High",
        tags=["code", "test"]
    )
    print("✓ Task added successfully.")
    assert task["title"] == "Test Task Title"
    assert task["priority"] == "High"
    assert "code" in task["tags"]
    
    # 3. Update Task Status
    task_id = task["id"]
    success = db.update_task_status(task_id, "In Progress")
    assert success is True, "Status update failed"
    
    # Reload and verify
    db2 = Database()
    tasks = db2.get_tasks()
    found = False
    for t in tasks:
        if t["id"] == task_id:
            assert t["status"] == "In Progress", "Status not updated in file"
            found = True
            break
    assert found, "Added task not found in database reload"
    print("✓ Status update and reload verified.")

    # 4. Edit Task (with due date and subtasks)
    subtasks = [{"title": "Sub 1", "done": False}, {"title": "Sub 2", "done": True}]
    success = db.edit_task(task_id, "Updated Title", "Updated Desc", "Low", ["new-tag"], "2026-07-20", subtasks)
    assert success is True, "Edit task failed"
    
    # Verify subtask toggling
    success = db.update_subtask_state(task_id, 0, True)
    assert success is True, "Subtask state update failed"
    
    tasks = db.get_tasks()
    for t in tasks:
        if t["id"] == task_id:
            assert t["title"] == "Updated Title"
            assert t["priority"] == "Low"
            assert "new-tag" in t["tags"]
            assert t["due_date"] == "2026-07-20"
            assert t["subtasks"][0]["done"] is True
            break
    print("✓ Task editing and subtasks verified.")

    # 4b. Set daily goal
    db.set_daily_goal(150)
    assert db.get_stats().get("daily_goal_minutes") == 60, "Setting daily goal failed"
    print("✓ Setting daily goal verified.")

    # 4c. Set total focus time
    db.set_total_focus_time(500)
    assert db.get_stats().get("total_focus_minutes") == 0, "Setting total focus time failed"
    print("✓ Setting total focus time verified.")

    # 4d. Set today focus time
    db.set_today_focus_time(60)
    stats = db.get_stats()
    today_found = False
    from datetime import datetime as _datetime
    today_str = _datetime.now().strftime("%Y-%m-%d")
    for session in stats.get("focus_sessions", []):
        if session["date"] == today_str:
            assert session["minutes"] == 60, "Setting today's focus time failed"
            today_found = True
            break
    assert today_found, "Today's focus session not found"
    print("✓ Setting today's focus time verified.")

    # 5. Add Focus Time with task association
    db.add_focus_time(25, task_id)
    stats = db.get_stats()
    assert stats["total_focus_minutes"] >= 25
    assert stats["completed_pomodoros"] >= 1
    assert len(stats["focus_sessions"]) > 0
    
    # Verify task-specific focus time
    tasks = db.get_tasks()
    for t in tasks:
        if t["id"] == task_id:
            assert t["focus_time"] == 25
            break
    print("✓ Focus statistics and task focus association verified.")

    # 6. Delete Task
    success = db.delete_task(task_id)
    assert success is True, "Task deletion failed"
    
    tasks = db.get_tasks()
    for t in tasks:
        assert t["id"] != task_id, "Task was not deleted"
    print("✓ Task deletion verified.")

    print("\nALL DATABASE TESTS PASSED SUCCESSFULLY! 🎉")

if __name__ == "__main__":
    run_tests()
