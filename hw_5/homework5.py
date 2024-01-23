from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pandas as pd


app = FastAPI()
templates = Jinja2Templates(directory="templates")
tasks = []

class Task(BaseModel):
    id: int
    head: str
    description: str
    status: str


@app.get("/tasks/", response_class=HTMLResponse)
async def show_task(request: Request):
    table = pd.DataFrame([vars(task) for task in tasks]).to_html()
    return templates.TemplateResponse("task.html", {"request": request, "table": table})


@app.get("/tasks/{id}")
async def read_task(request: Request, id: int):
    for i, stor_task in enumerate(tasks):
        if stor_task.id == id:
            table = pd.DataFrame([stor_task]).to_html()
            return templates.TemplateResponse("task.html", {"request": request, "table": table})
    return {"error": "Task not found"}


@app.post("/tasks/", response_model=Task)
async def create_user(task: Task):
    tasks.append(task)
    return task

@app.put("/task/{id}", response_model=Task)
async def put_user(id: int, task: Task):
    for i, stor_task in enumerate(tasks):
        if stor_task.id == task.id:
            task.id = id
            tasks[i] = task
            return task

@app.delete("/task/{id}", response_class=HTMLResponse)
async def delet_task(request: Request, id: int):
    for i, stor_task in enumerate(tasks):
        if stor_task.id == id:
            return pd.DataFrame([vars(tasks.pop(i))]).to_html()