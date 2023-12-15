from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def get_data():
    data = {"message": "Hello from the backend!"}
    return jsonify(data)