import gradio as gr
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/todos"
MAX_TASKS = 50

def fetch_tasks():
    try:
        return requests.get(API_URL).json()
    except:
        return []

def create_task(task, due_timestamp):
    due_date = datetime.fromtimestamp(due_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    requests.post(API_URL, json={"task": task, "due_date": due_date})
    return fetch_tasks()

def delete_task(task_id):
    requests.delete(f"{API_URL}/{task_id}")
    return fetch_tasks()

def render(tasks):
    md_updates, btn_updates, row_updates, id_updates = [], [], [], []
    for i in range(MAX_TASKS):
        if i < len(tasks):
            task = tasks[i]
            md_updates.append(gr.update(value=f"**{task['task']}**\n🕒 Due: {task['due_date']}", visible=True))
            btn_updates.append(gr.update(visible=True))
            row_updates.append(gr.update(visible=True))
            id_updates.append(gr.update(value=task["id"], visible=False))
        else:
            md_updates.append(gr.update(visible=False))
            btn_updates.append(gr.update(visible=False))
            row_updates.append(gr.update(visible=False))
            id_updates.append(gr.update(visible=False))
    return md_updates + btn_updates + row_updates + id_updates

with gr.Blocks() as app:
    gr.Markdown("## 📝 To-Do List")

    with gr.Row():
        task_input = gr.Textbox(label="New Task", placeholder="Enter task...")
        due_input = gr.DateTime(label="Due Date & Time")

    add_btn = gr.Button("➕ Add Task")

    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown("### Tasks")
        with gr.Column(scale=1):
            refresh_btn = gr.Button("🔄 Refresh")

    markdowns, btns, rows, ids_hidden = [], [], [], []

    for _ in range(MAX_TASKS):
        with gr.Row(visible=False) as row:
            md = gr.Markdown()
            task_id = gr.Number(visible=False)
            btn = gr.Button("🗑️")
            btn.click(fn=delete_task, inputs=[task_id], outputs=[]).then(
                fn=lambda: render(fetch_tasks()), outputs=[]
            )
            markdowns.append(md)
            btns.append(btn)
            rows.append(row)
            ids_hidden.append(task_id)

    all_outputs = markdowns + btns + rows + ids_hidden

    add_btn.click(fn=create_task, inputs=[task_input, due_input], outputs=[]).then(
        fn=lambda: render(fetch_tasks()), outputs=all_outputs
    )

    refresh_btn.click(fn=lambda: render(fetch_tasks()), outputs=all_outputs)
    app.load(fn=lambda: render(fetch_tasks()), outputs=all_outputs)

app.launch()
