import os
from flask import Flask
from functions import jsonsheet,addReserva,jsonReservas
app = Flask(__name__)
import json
from flask import jsonify,request, make_response
from flask_cors import CORS
CORS(app)
@app.route('/')
def hello():
    data=jsonsheet()
    print(data)
    return make_response(jsonify(data), 200)

@app.route('/insert', methods=['GET', 'POST'])
def parse_request():
    if request.method == 'POST':
        value={  "email":request.form.get('email'),
                "emailCandidato":request.form.get('emailCandidato'),
                "naCandi":request.form.get('naCandi'),
                "lkCandi":request.form.get('lkCandi'), 
                "tcandi":request.form.getlist('tcandi[]'),
                "tperfil":request.form.getlist('tperfil[]'),
                "idReserva":request.form.get('idReserva'),
                "comment":request.form.get('comment')
                }
        addReserva(value)
    return 'ok', 200 

@app.route('/reservas')
def reserva():
    data=jsonReservas()
    return make_response(jsonify(data), 200)
@app.route('/quit')
def _quit():
    os._exit(0)

