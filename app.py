import os
from flask import Flask
from functions import *
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
@app.route('/Informe')
def Informe():
    data=InformeRechazados()
    print(data)
    return make_response(jsonify(data), 200)

@app.route('/insert', methods=['GET', 'POST'])
def insertreserva():
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

@app.route('/solicitudInforme', methods=['GET', 'POST'])
def solinforme():
    if request.method == 'POST':
        value={  "EmailInf":request.form.get('emailInf'),
                "EMailCandidatoInf":request.form.get('emailCandidatoInf'),
                "NombreyApellidodelCandidatoInf":request.form.get('naCandiInf'),
                "EsSourceInf":request.form.get('EsSourceInf'),
                "IdsaEnviarInf": request.form.get('idReservaInf'),
                "RemuneracionPretendidaMensualInf":request.form.get('remuneracionPretendidaMensualInf'),
                "NiveldeInglesInf":request.form.getlist('NiveldeInglesInf'),
                "LocacionInf":request.form.getlist('locacionInf'),
                "LKCandiInf":request.form.get('lkCandiInf'),
                "TecnoCandiInf":request.form.getlist('TecnoCandiInf[]'),
                "TpCandiInf":request.form.get('TpCandiInf[]'),
                "CommentInf":request.form.get('commentInf'),
                 "informeEntEsp":request.form.get('informeEntEspInf'),
                 "informeEntIng":request.form.get('informeEntIngInf')
                }
        addInforme(value)
    return 'ok', 200

@app.route('/reservas')
def reserva():
    data=jsonReservas()
    return make_response(jsonify(data), 200)
@app.route('/getInformesArevisar')
def infarevisar():
    data=getInformesArevisar()
    return make_response(jsonify(data), 200)

@app.route('/busquedas')
def busqueda():
    data=busquedas()
    return make_response(jsonify(data), 200)
@app.route('/busquedasPrioritarias')
def busquedasPrio():
    data=busquedasPrioritarias()
    return make_response(jsonify(data), 200)

@app.route('/revisarAprobado', methods=['GET', 'POST']) 
def revisar():
    if request.method == 'POST':
        value = {
                "StatusEnBaseInf": request.form.get('stEnBaseInf'),
                "EmailInf": request.form.get('emailInf'),
                "EMailCandidatoInf": request.form.get('emailCandiInf'),
                "IdsaEnviarInf": request.form.get('idInf'),
                "EsSourceInf": request.form.get('esSourceInf'),
                "NombreyApellidodelCandidatoInf": request.form.get('nombreCandiInf'),
                "RemuneracionPretendidaMensualInf": request.form.get('remuneracionPretendida'),
                "NiveldeInglesInf": request.form.get('nivelInglesInf'),
                "LocacionInf": request.form.get('locacionInf'),
                "LKCandiInf": request.form.get('lkCandiInf'),
                "TecnoCandiInf": request.form.get('tecCandiInf'),
                "TpCandiInf": request.form.get('tPCandiInf'),
                "CommentInf": request.form.get('comentInf'),
                "CvEspanolInf": request.form.get('cvEspInf'),
                "informeEntEsp": request.form.get('infEntEsp'),
                "CvInglesInf": request.form.get('cvIngInf'),
                "informeEntIng": request.form.get('infEntIng'),
                "MotivvoRechazoInf": request.form.get('motivoRechInf'),
            }      
    if request.form.get('status')=='True':
        data=revisarAprob(value)
    else:
        data=revisarRechaz(value)    
    return make_response(jsonify(data), 200)

@app.route('/Getreservas',methods=['GET', 'POST'])
def reservaemail():
    if request.method == 'POST':
        email=request.form.get('emailCandidato')
        data=devolverReserva(email)
        return make_response(jsonify(data), 200)
@app.route('/quit')
def _quit():
    os._exit(0)

@app.route('/modreserva', methods=['GET', 'POST'])
def modreserva():
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
        modificarReservar(value)
    return 'ok', 200
