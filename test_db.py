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

    # 4. Edit Task
    success = db.edit_task(task_id, "Updated Title", "Updated Desc", "Low", ["new-tag"])
    assert success is True, "Edit task failed"
    tasks = db.get_tasks()
    for t in tasks:
        if t["id"] == task_id:
            assert t["title"] == "Updated Title"
            assert t["priority"] == "Low"
            assert "new-tag" in t["tags"]
            break
    print("✓ Task editing verified.")

    # 5. Add Focus Time
    db.add_focus_time(25)
    stats = db.get_stats()
    assert stats["total_focus_minutes"] >= 25
    assert stats["completed_pomodoros"] >= 1
    assert len(stats["focus_sessions"]) > 0
    print("✓ Focus statistics operations verified.")

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
