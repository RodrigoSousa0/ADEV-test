import gradio as gr
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/todos"

def load_todos():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    return []

def add_task(task, due_timestamp):
    due_date = datetime.fromtimestamp(due_timestamp)
    due_date_str = due_date.strftime("%Y-%m-%d %H:%M:%S")
    requests.post(API_URL, json={"task": task, "due_date": due_date_str})
    return update_task_table()

def delete_task_and_reload(task_id):
    requests.delete(f"{API_URL}/{task_id}")
    return update_task_table()

def update_task_table():
    tasks = load_todos()
    return [[t["task"], t["due_date"]] for t in tasks]

with gr.Blocks() as app:
    gr.Markdown("## 📝 To-Do List App")

    with gr.Row():
        task_input = gr.Textbox(placeholder="New task...", label="Task")
        due_input = gr.Textbox(label="Due Date (YYYY-MM-DD HH:MM:SS)", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    add_btn = gr.Button("➕ Add Task")

    with gr.Row():
        gr.Markdown("### Tasks")
        refresh_btn = gr.Button("🔄 Refresh")

    task_list = gr.DataFrame(headers=["Task", "Due Date"], interactive=False, row_count=(1, "dynamic"))

    del_input = gr.Number(label="Enter Row Index to Delete (starting from 0)", precision=0)
    del_btn = gr.Button("🗑️ Delete Selected")

    def handle_add(task, due_str):
        if task and due_str:
            due_dt = datetime.strptime(due_str, "%Y-%m-%d %H:%M:%S")
            due_timestamp = due_dt.timestamp()
            return add_task(task, due_timestamp)
        return update_task_table()

    def handle_delete(row_index):
        tasks = load_todos()
        if 0 <= row_index < len(tasks):
            task_id = tasks[row_index]["id"]
            return delete_task_and_reload(task_id)
        return update_task_table()

    add_btn.click(fn=handle_add, inputs=[task_input, due_input], outputs=task_list)
    refresh_btn.click(fn=update_task_table, outputs=task_list)
    del_btn.click(fn=handle_delete, inputs=del_input, outputs=task_list)

    app.load(fn=update_task_table, outputs=task_list)

app.launch()
