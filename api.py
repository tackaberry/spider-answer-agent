from flask import Flask, request
from .answer import getAnswer

app = Flask(__name__)

@app.route("/", methods=[ "POST"])
def answer():
    request_data = request.get_json()
    print(request_data)
    answer = getAnswer(request_data["question"])
    return answer