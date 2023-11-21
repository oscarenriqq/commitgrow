import os
from todoist_api_python.api import TodoistAPI

def get_todoist_tasks(todoist_token, label='commitgrow'):
    
    todoist_conn = TodoistAPI(todoist_token)
    
    response = []
    tasks = todoist_conn.get_tasks(label=label)
    for task in tasks:
        response.append({
            "task_id": task.id,
            "task_content": task.content,
            "task_url": task.url
        })
    return response

def get_todoist_task(todoist_token, task_id: str):
    
    todoist_conn = TodoistAPI(todoist_token)
    
    task = todoist_conn.get_task(task_id=task_id)
    
    return {
        "task_id": task.id,
        "task_content": task.content,
        "task_url": task.url,
        "task_due": task.due.date if task.due is not None else None,
        "task_project_id": task.project_id,
        "task_section_id": task.section_id,
        "task_description": task.description,
        "task_priority": task.priority,
    }