from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient
import uuid
import hashlib
import json

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
collection = db["todo_items"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "admin":
        return redirect("/todo")
    return "Invalid Credentials"

@app.route("/todo")
def todo():
    return render_template("todo.html")

@app.route("/api")
def api():
    with open("data.json") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/submittodoitem", methods=["POST"])
def submit_todo():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    todo_item = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    collection.insert_one(todo_item)
    return "Item Saved Successfully"

if __name__ == "__main__":
    app.run(debug=True)
