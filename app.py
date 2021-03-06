from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
from datetime import date
from bson import ObjectId

app = Flask(__name__)
app.config[
    "MONGO_URI"
] = "Your URI Here"

mongo = PyMongo()
mongo.init_app(app)

tasks_collection = mongo.db.todoapp


@app.post("/")
def add_todo():
    new_task = request.form["content"]
    data = {"content": new_task, "date_created": str(date.today()), "complete": False}
    tasks_collection.insert_one(data)
    return redirect("/")


@app.get("/")
def index():
    tasks = tasks_collection.find()
    return render_template("index.html", tasks=tasks)


@app.get("/update/<oid>")
def update_get(oid:str):
    task = tasks_collection.find_one({"_id": ObjectId(oid)})
    return render_template("update.html", task=task)


@app.post("/update/<oid>")
def update_post(oid:str):
    
    content = request.form["content"]
    tasks_collection.update_one({"_id": ObjectId(oid)}, {"$set": {"content": content}})
    return redirect("/")


@app.route('/delete/<oid>')
def delete(oid:str):
    
    tasks_collection.delete_one({'_id': ObjectId(oid)})
    return redirect('/')


@app.route('/complete/<oid>')
def mark_complete(oid:str):
    
    task = tasks_collection.find_one({'_id': ObjectId(oid)})
    task["complete"] = True
    tasks_collection.save(task)
    return redirect ('/')

if __name__ == "__main__":
    app.run(debug=True)

# source C:/Users/snish/AppData/Local/pypoetry/Cache/virtualenvs/todo_app-Xsaj7QwE-py3.9/Scripts/activate
