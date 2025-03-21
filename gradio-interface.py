import gradio as gr
import requests

API_URL = "http://backend:8000/todos"

def load_todos():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return [f"{item['id']}: {item['task']}" for item in response.json()]
    return ["Error loading todos"]

def add_todo(task, task_id):
    requests.post(API_URL, json={"id": int(task_id), "task": task})
    return load_todos()

def delete_todo(task_id):
    requests.delete(f"{API_URL}/{int(task_id)}")
    return load_todos()

with gr.Blocks() as app:
    task_input = gr.Textbox(label="New Task")
    id_input = gr.Number(label="Task ID", precision=0)
    add_button = gr.Button("Add Task")
    delete_button = gr.Button("Delete Task")
    todo_list = gr.List(label="To-Do List")

    add_button.click(add_todo, inputs=[task_input, id_input], outputs=todo_list)
    delete_button.click(delete_todo, inputs=[id_input], outputs=todo_list)

    app.load(load_todos, outputs=todo_list)

app.launch(server_name="0.0.0.0", server_port=7860)
