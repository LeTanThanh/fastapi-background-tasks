from fastapi import FastAPI
from fastapi import Path
from fastapi import BackgroundTasks
from fastapi import Depends
from typing import Annotated

app = FastAPI()

def write_log(message=""):
  with open("log.txt", mode="a") as log:
    log.write(message)

def get_query(background_tasks: BackgroundTasks, q: str | None = None):
  if q:
    message = f"found query: {q}\n"
    background_tasks.add_task(write_log, message = message)
  return q

@app.get("/")
async def home():
  return {"message": "hello"}

# Using BackgroundTasks
"""
@app.post("/send_notification/{email}")
async def send_notification(email: Annotated[str, Path()], background_tasks: BackgroundTasks):
  background_tasks.add_task(write_notification, email = email, message = "some notification")
  return {"message": "Notification sent in the background"}
"""

# Dependency Injection
@app.post("/send_notification/{email}")
async def send_notification(
  email: Annotated[str, Path()],
  query: Annotated[str, Depends(get_query)],
  background_tasks: BackgroundTasks
):
  message = f"message to {email}\n"
  background_tasks.add_task(write_log, message)

  return {"message": "Message sent"}
