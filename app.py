from flask import Flask
from functions import jsonsheet
app = Flask(__name__)
import json
from flask import jsonify, make_response
@app.route('/')
def hello():
    data=jsonsheet()
    print(data)
    return make_response(jsonify(data), 200)
