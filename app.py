import os
from flask import Flask,request,current_app, flash, jsonify, make_response, redirect, request, url_for
from mysql import *
from functions import *
import json
from flask_cors import CORS,cross_origin
from urllib.parse import unquote
import io as BytesIO
import base64 as b64
from codecs import encode
app = Flask(__name__)
CORS(app)
import socket
myhost = socket.gethostname()
if 'DESKTOP-EKG5FVQ'==myhost:
    app.run(debug=True)
else:
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
        addInforme(value)
    return 'ok', 200

@cross_origin()
@app.route('/base64')
def base64():
    id=request.form.get('id')
    email=request.form.get('email')
    emailc=request.form.get('emailc')
    args = request.args
    if id is None:
        id = args.get('id')
        email = args.get('email')
        emailc = args.get('emailc')
    data=base64decode(id,email,emailc)
    data = 'JVBERi0xLjMKJf////8KOCAwIG9iago8PAovVHlwZSAvRXh0R1N0YXRlCi9jYSAxCj4+CmVuZG9iago3IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgMSAwIFIKL01lZGlhQm94IFswIDAgNTk1LjI4MDAyOSA4NDEuODkwMDE1XQovQ29udGVudHMgNSAwIFIKL1Jlc291cmNlcyA2IDAgUgo+PgplbmRvYmoKNiAwIG9iago8PAovUHJvY1NldCBbL1BERiAvVGV4dCAvSW1hZ2VCIC9JbWFnZUMgL0ltYWdlSV0KL0V4dEdTdGF0ZSA8PAovR3MxIDggMCBSCj4+Ci9YT2JqZWN0IDw8Ci9JMSA5IDAgUgo+PgovRm9udCA8PAovRjIgMTAgMCBSCi9GNCAxMSAwIFIKPj4KPj4KZW5kb2JqCjEzIDAgb2JqCihyZWFjdC1wZGYpCmVuZG9iagoxNCAwIG9iagoocmVhY3QtcGRmKQplbmRvYmoKMTUgMCBvYmoKKEQ6MjAyMjEyMjcxOTE5MDBaKQplbmRvYmoKMTIgMCBvYmoKPDwKL1Byb2R1Y2VyIDEzIDAgUgovQ3JlYXRvciAxNCAwIFIKL0NyZWF0aW9uRGF0ZSAxNSAwIFIKPj4KZW5kb2JqCjE3IDAgb2JqCjw8Ci9UeXBlIC9Gb250RGVzY3JpcHRvcgovRm9udE5hbWUgL1VWRFRUTitSb2JvdG8tUmVndWxhcgovRmxhZ3MgNAovRm9udEJCb3ggWy03MzYuODE2NDA2IC0yNzAuOTk2MDk0IDExNDguNDM3NSAxMDU2LjE1MjM0NF0KL0l0YWxpY0FuZ2xlIDAKL0FzY2VudCA5MjcuNzM0Mzc1Ci9EZXNjZW50IC0yNDQuMTQwNjI1Ci9DYXBIZWlnaHQgNzEwLjkzNzUKL1hIZWlnaHQgNTI4LjMyMDMxMwovU3RlbVYgMAovRm9udEZpbGUyIDE2IDAgUgo+PgplbmRvYmoKMTggMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL0NJREZvbnRUeXBlMgovQmFzZUZvbnQgL1VWRFRUTitSb2JvdG8tUmVndWxhcgovQ0lEU3lzdGVtSW5mbyA8PAovUmVnaXN0cnkgKEFkb2JlKQovT3JkZXJpbmcgKElkZW50aXR5KQovU3VwcGxlbWVudCAwCj4+Ci9Gb250RGVzY3JpcHRvciAxNyAwIFIKL1cgWzAgWzkwOCA1OTYuNjc5Njg4IDU1MS4yNjk1MzEgMzM4LjM3ODkwNiA1NTEuNzU3ODEzIDU3MC4zMTI1IDI0Ny41NTg1OTQgNTYxLjAzNTE1NiA1MjkuNzg1MTU2IDU0My45NDUzMTMgNTYzLjk2NDg0NCAyNDIuNjc1NzgxIDI0Ny4wNzAzMTMgMjQyLjE4NzUgNTYxLjUyMzQzOCA1NjEuNTIzNDM4IDQxMi4xMDkzNzUgNTYxLjUyMzQzOCA1NjEuNTIzNDM4IDg3My4wNDY4NzUgMjQyLjY3NTc4MSA1MjMuNDM3NSA1NjEuMDM1MTU2IDY1Mi4zNDM3NSA0ODQuMzc1IDY1NS43NjE3MTkgNTcwLjMxMjUgNjgxLjE1MjM0NCA1MzguMDg1OTM4IDUxNS42MjUgNjUwLjg3ODkwNiA2MjIuNTU4NTk0IDI3NS44Nzg5MDYgNTkzLjI2MTcxOSA2MzAuODU5Mzc1IDU2MS41MjM0MzggNTYxLjUyMzQzOCA1NjEuNTIzNDM4IDU2MS41MjM0MzggNjE1LjcyMjY1NiA1NjguMzU5Mzc1IDcxMi44OTA2MjUgNjg3LjUgNjM2LjIzMDQ2OSAyNzEuOTcyNjU2IDY4Ny41IDY0OC40Mzc1IDU2MS4wMzUxNTYgODc2LjQ2NDg0NCAzMjYuNjYwMTU2XV0KPj4KZW5kb2JqCjEwIDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMAovQmFzZUZvbnQgL1VWRFRUTitSb2JvdG8tUmVndWxhcgovRW5jb2RpbmcgL0lkZW50aXR5LUgKL0Rlc2NlbmRhbnRGb250cyBbMTggMCBSXQovVG9Vbmljb2RlIDE5IDAgUgo+PgplbmRvYmoKMjEgMCBvYmoKPDwKL1R5cGUgL0ZvbnREZXNjcmlwdG9yCi9Gb250TmFtZSAvWU1EV0hFK1JvYm90by1Cb2xkCi9GbGFncyA0Ci9Gb250QkJveCBbLTcyNi41NjI1IC0yNzAuOTk2MDk0IDExOTAuOTE3OTY5IDEwNTYuMTUyMzQ0XQovSXRhbGljQW5nbGUgMAovQXNjZW50IDkyNy43MzQzNzUKL0Rlc2NlbnQgLTI0NC4xNDA2MjUKL0NhcEhlaWdodCA3MTAuOTM3NQovWEhlaWdodCA1MjguMzIwMzEzCi9TdGVtViAwCi9Gb250RmlsZTIgMjAgMCBSCj4+CmVuZG9iagoyMiAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvQ0lERm9udFR5cGUyCi9CYXNlRm9udCAvWU1EV0hFK1JvYm90by1Cb2xkCi9DSURTeXN0ZW1JbmZvIDw8Ci9SZWdpc3RyeSAoQWRvYmUpCi9PcmRlcmluZyAoSWRlbnRpdHkpCi9TdXBwbGVtZW50IDAKPj4KL0ZvbnREZXNjcmlwdG9yIDIxIDAgUgovVyBbMCBbOTA4IDY1NC4yOTY4NzUgNTY1LjQyOTY4OCA4NjUuNzIyNjU2IDU2Mi45ODgyODEgMzY0Ljc0NjA5NCA1NjIuOTg4MjgxIDUzNi4xMzI4MTMgNTYwLjA1ODU5NCAzMzcuODkwNjI1IDU0MC41MjczNDQgMjQ5LjAyMzQzOCA1NjMuNDc2NTYzIDY3Mi44NTE1NjMgNTE0LjE2MDE1NiAyNjUuMTM2NzE5IDU3MC44MDA3ODEgNTIxLjQ4NDM3NSA1NjUuNDI5Njg4IDYxOC42NTIzNDQgNTU5LjU3MDMxMyA1NDEuNTAzOTA2IDI4Mi4yMjY1NjMgNzA2LjA1NDY4OCAyOTAuNTI3MzQ0IDUzNi4xMzI4MTMgNTQ3Ljg1MTU2MyA1NTkuNTcwMzEzIDcwNi41NDI5NjkgNjE0Ljc0NjA5NCAyNjUuMTM2NzE5IDUwMS45NTMxMjUgNjQ5LjkwMjM0NF1dCj4+CmVuZG9iagoxMSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTAKL0Jhc2VGb250IC9ZTURXSEUrUm9ib3RvLUJvbGQKL0VuY29kaW5nIC9JZGVudGl0eS1ICi9EZXNjZW5kYW50Rm9udHMgWzIyIDAgUl0KL1RvVW5pY29kZSAyMyAwIFIKPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL0NhdGFsb2cKL1BhZ2VzIDEgMCBSCi9OYW1lcyAyIDAgUgovVmlld2VyUHJlZmVyZW5jZXMgNCAwIFIKPj4KZW5kb2JqCjEgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9Db3Vu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'
    data = encode(data, 'utf-8')
    content =b64.decodebytes(data)
    response=make_response( content)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=clau.pdf'
    response.headers['Content-Transfer-Encoding'] = 'binary'
    return response


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
