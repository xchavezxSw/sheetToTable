import os
from flask import Flask,request,current_app, flash, jsonify, make_response, redirect, request, url_for
from mysql import *
from functions import *
import json
from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
@cross_origin()
def hello():
    data=jsonsheet()
    print(data)
    return make_response(jsonify(data), 200)
@app.route('/Informe')
@cross_origin()
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
        devuelvo=addReserva(value)
    if devuelvo=='403':
        return 'el candidato fue contratado con anterioridad', 403
    else:
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
    value={  }
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
@app.route('/getPermitido',methods=['GET', 'POST'])
def permitido():
    if request.method == 'POST':
        email = request.form.get('email')
        data = permitidof(email)
        if data['permitido']:
            return make_response(jsonify(data), 200)
        else:
            return make_response(jsonify(data), 403)

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
"""conexion a mysq"""
@app.route('/getCliente')
def getencliente():
    args = request.args
    usuario=args.get('usuario')
    if usuario!='' or usuario is not None:
        data=encliente(usuario)
    else:
        data=encliente()
    return make_response(jsonify(data), 200)

@app.route('/getReservados')
def getreservados():

    args = request.args
    usuario=args.get('usuario')
    if usuario!='' or usuario is not None:
        data=reservados(usuario)
    else:
        data=reservados()
    return make_response(jsonify(data), 200)

@app.route('/getmetricas')
def getmetrica():
    args = request.args
    usuario = args.get('usuario')
    if usuario != '' or usuario is not None:
        data = metrica(usuario)
    else:
        data = metrica()
    return make_response(jsonify(data), 200)

@app.route('/getContratados')
def getContratados():
    args = request.args
    usuario = args.get('usuario')
    if usuario != '' or usuario is not None:
        data=contratadosFun(usuario)
    else:
        data=contratadosFun()

    return make_response(jsonify(data), 200)

@app.route('/getCambioEstado',methods=['GET', 'POST'])
def getcambiostatus():
    if request.method == 'POST':
        emailCandi=request.form.get('emailCandidatoSt')
        id = request.form.get('idSt')
        data=devolvercambiostado(emailCandi, id)
        return make_response(jsonify(data), 200)


@app.route('/cambioEstado',methods=['GET', 'POST'])
def cambioEstado():
    if request.method == 'POST':
        emailCandi = request.form.get('emailCandidatoSt')
        idSt = request.form.get('idSt')
        emailSt = request.form.get('emailSt')
        statusSt = request.form.get('statusSt')
        salarioMensualAcordadoSt=request.form.get('salarioMensualAcordadoSt')
        fechaIngresoSt=request.form.get('fechaIngresoSt')
        comentariosSt=request.form.get('comentariosSt')
        salarioMensualOfrecidoClienteSt=request.form.get('salarioMensualOfrecidoClienteSt')
        salarioMensualPretendidoSt=request.form.get('salarioMensualPretendidoSt')
        motivoFinCandi=request.form.get('motivoFinCandi')
        motivoFinCliente=request.form.get('motivoFinCliente')

        if statusSt not in [ '11','12']:
            data=insertEstado(emailCandi,idSt,emailSt,statusSt)
            modificarStatus(emailCandi, idSt, emailSt, statusSt)
        if statusSt == '11':
            data = insertEstado(emailCandi, idSt, emailSt, statusSt)
            data=insertEstado11(emailCandi,idSt,emailSt,statusSt,salarioMensualAcordadoSt,fechaIngresoSt,comentariosSt)
            modificarStatus11(emailCandi,idSt,emailSt,statusSt,salarioMensualAcordadoSt,fechaIngresoSt,comentariosSt)
        if statusSt == '12':
            data = insertEstado(emailCandi, idSt, emailSt, statusSt)
            data=insertEstado12(emailCandi,idSt,emailSt,statusSt,salarioMensualOfrecidoClienteSt,salarioMensualPretendidoSt,motivoFinCandi,motivoFinCliente)
            modificarStatus12(emailCandi,idSt,emailSt,statusSt,salarioMensualOfrecidoClienteSt,salarioMensualPretendidoSt,motivoFinCandi,motivoFinCliente)


        return make_response(jsonify(None), 200)


@app.route('/setcookie', methods=['POST', 'GET'])
@cross_origin()
def setcookie():
    if request.method == 'POST':
        user = request.form['user']
        password=request.form['password']
    validar,rol=login(user, password)
    if validar >=1:
        resp =make_response(jsonify(json.loads(json.dumps(['logueado',rol,user]).encode('utf-8').decode('ascii'))), 200)
        resp.set_cookie('userID', user)
        resp.set_cookie('rol', rol)
        return resp
    else:
        return make_response(jsonify(None), 403)


@app.route('/getcookie', methods=['POST', 'GET'])
def getcookie():
   name = request.cookies.get('userID')
   if name is None:
       return  make_response(jsonify(json.loads(json.dumps([None]).encode('utf-8').decode('ascii'))), 200)
   else:
       return make_response(jsonify(json.loads(json.dumps([name]).encode('utf-8').decode('ascii'))), 200)
