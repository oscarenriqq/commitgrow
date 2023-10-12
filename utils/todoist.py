import os
from todoist_api_python.api import TodoistAPI

todoist_conn = TodoistAPI(os.getenv("TODOIST_ACCESS_TOKEN"))

def get_todoist_tasks(label='commit-grow'):
    response = []
    tasks = todoist_conn.get_tasks(label=label)
    for task in tasks:
        response.append({
            "task_id": task.id,
            "task_content": task.content,
            "task_url": task.url
        })
    return response

def get_todoist_task(task_id: str):
    task = todoist_conn.get_task(task_id=task_id)
    return {
        "task_id": task.id,
        "task_content": task.content,
        "task_url": task.url,
        "task_due": task.due.date,
        "task_project_id": task.project_id,
        "task_section_id": task.section_id,
        "task_description": task.description,
        "task_priority": task.priority,
    }