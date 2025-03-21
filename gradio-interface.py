import gradio as gr
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/todos"

def fetch_tasks():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []

def create_task(task, due_timestamp):
    due_date = datetime.fromtimestamp(due_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    requests.post(API_URL, json={"task": task, "due_date": due_date})
    return render_task_markdown()

def render_task_markdown():
    tasks = fetch_tasks()
    if not tasks:
        return "**No tasks found.**"
    return "\n\n".join(
        [f"**{t['task']}**  \n🕒 Due: {t['due_date']}" for t in tasks]
    )

with gr.Blocks() as app:
    gr.Markdown("## 📝 To-Do List")

    with gr.Row():
        task_input = gr.Textbox(label="New Task", placeholder="Enter task...")
        due_input = gr.DateTime(label="Due Date & Time")
        add_btn = gr.Button("➕ Add Task")

    refresh_btn = gr.Button("🔄 Refresh")

    task_display = gr.Markdown()

    add_btn.click(fn=create_task, inputs=[task_input, due_input], outputs=task_display)
    refresh_btn.click(fn=render_task_markdown, outputs=task_display)
    app.load(fn=render_task_markdown, outputs=task_display)

app.launch()
