from fastapi import FastAPI
from fastapi import Path
from fastapi import BackgroundTasks

from typing import Annotated

app = FastAPI()

def write_notification(email: str, message=""):
  with open("log.txt", mode="w") as email_file:
    content = f"notification for {email}: {message}"
    email_file.write(content)

@app.get("/")
async def home():
  return {"message": "hello"}

# Using BackgroundTasks

@app.post("/send_notification/{email}")
async def send_notification(email: Annotated[str, Path()], background_tasks: BackgroundTasks):
  background_tasks.add_task(write_notification, email = email, message = "some notification")
  return {"message": "Notification sent in the background"}
