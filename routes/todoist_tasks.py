from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils import todoist

task_route = APIRouter(prefix="/api")

@task_route.get("/todoist-tasks")
def get_tasks():
    return JSONResponse(status_code=200, content=todoist.get_todoist_tasks())

@task_route.get("/todoist-task/{id}")
def get_tasks(id: str):
    return JSONResponse(status_code=200, content=todoist.get_todoist_task(task_id=id))