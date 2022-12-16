import os
from flask import Flask,request,current_app, flash, jsonify, make_response, redirect, request, url_for
from mysql import *
from functions import *
import json
from flask_cors import CORS,cross_origin
from urllib.parse import unquote
app = Flask(__name__)
CORS(app)

from OpenSSL import SSL
context = SSL.Context(SSL.TLSv1_2_METHOD)
context.use_privatekey_file('/root/ssl/conexion.key')
context.use_certificate_file('/root/ssl/conexion.crt')  
app.run(debug=True, ssl_context=context        )

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', ' GET, POST')
    return response

@cross_origin()
@app.route('/')
def hello():
    data=jsonsheet()
    print(data)
    return make_response(jsonify(data), 200)

@cross_origin()
@app.route('/Informe')
def Informe():
    data=InformeRechazados()
    print(data)
    return make_response(jsonify(data), 200)

@cross_origin()
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
        if devuelvo == '410':
            return 'el candidato esta reservado o en pertenencia con otro reclutador', 410
        else:
            return 'ok', 200
@cross_origin()
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
        print(value)
        addInforme(value)
    return 'ok', 200

@cross_origin()
@app.route('/reservas')
def reserva():
    data=jsonReservas()
    return make_response(jsonify(data), 200)

@cross_origin()
@app.route('/getInformesArevisar')
def infarevisar():
    data=getInformesArevisar()
    return make_response(jsonify(data), 200)

@cross_origin()
@app.route('/busquedas')
def busqueda():
    data=busquedas()
    return make_response(jsonify(data), 200)

@cross_origin()
@app.route('/busquedasPrioritarias')
def busquedasPrio():
    data=busquedasPrioritarias()
    return make_response(jsonify(data), 200)
@cross_origin()
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
@cross_origin()
@app.route('/Getreservas',methods=['GET', 'POST'])
def reservaemail():
    if request.method == 'POST':
        email=request.form.get('emailCandidato')
        emailrec = request.form.get('email')
        data=devolverReserva(email)
        valor,reclutador = pertenencia(email)
        if valor != 'OK' and reclutador!=emailrec:
            data= '510'
        if data=='502':
            return make_response(jsonify(data), 502)

        else:
            if data == '510' and reclutador != emailrec:
                return make_response(jsonify(data), 502)
            else:
                return make_response(jsonify(data), 200)


@cross_origin()
@app.route('/getPermitido',methods=['GET', 'POST'])
def permitido():
    if request.method == 'POST':
        email = request.form.get('email')
        data = permitidof(email)
        if data['permitido']:
            return make_response(jsonify(data), 200)
        else:
            return make_response(jsonify(data), 403)
@cross_origin()
@app.route('/quit')
def _quit():
    os._exit(0)

@cross_origin()
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
@cross_origin()
@app.route('/getMisCandis')
def getMisCandis():
    args = request.args
    usuario=args.get('usuario')
    if usuario!='' or usuario is not None:
        usuario = unquote(usuario)
        data=miscandidatos(usuario)
    else:
        data=miscandidatos()
    return make_response(jsonify(data), 200)

@cross_origin()
@app.route('/getCliente')
def getencliente():
    args = request.args
    usuario=args.get('usuario')
    if usuario!='' or usuario is not None:
        usuario = unquote(usuario)
        data=encliente(usuario)
    else:
        data=encliente()
    return make_response(jsonify(data), 200)
@cross_origin()
@app.route('/getReservados')
def getreservados():

    args = request.args
    usuario=args.get('usuario')
    if usuario!='' or usuario is not None:
        usuario = unquote(usuario)
        data=reservados(usuario)
    else:
        data=reservados()
    return make_response(jsonify(data), 200)
@cross_origin()
@app.route('/getmetricas')
def getmetrica():
    args = request.args
    usuario = args.get('usuario')

    rol = args.get('rol')
    if usuario != '' or usuario is not None:
        usuario = unquote(usuario)
        data = metrica(usuario,rol)
    else:
        data = metrica()
    return make_response(jsonify(data), 200)
@cross_origin()
@app.route('/getContratados')
def getContratados():
    args = request.args
    usuario = args.get('usuario')
    if usuario != '' or usuario is not None:
        usuario = unquote('usuario')
        data=contratadosFun(usuario)
    else:
        data=contratadosFun()

    return make_response(jsonify(data), 200)
@cross_origin()
@app.route('/getCambioEstado',methods=['GET', 'POST'])
def getcambiostatus():
    if request.method == 'POST':
        emailCandi=request.form.get('emailCandidatoSt')
        id = request.form.get('idSt')
        data=devolvercambiostado(emailCandi, id)
        return make_response(jsonify(data), 200)

@cross_origin()
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

@cross_origin()
@app.route('/setcookie', methods=['POST', 'GET'])
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

@cross_origin()
@app.route('/getcookie', methods=['POST', 'GET'])
def getcookie():
   name = request.cookies.get('userID')
   if name is None:
       return  make_response(jsonify(json.loads(json.dumps([None]).encode('utf-8').decode('ascii'))), 200)
   else:
       name = unquote(name)
       return make_response(jsonify(json.loads(json.dumps([name]).encode('utf-8').decode('ascii'))), 200)
