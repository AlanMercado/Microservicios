# -*- coding: utf-8 -*-
#!/usr/bin/env python
#----------------------------------------------------------------------------------------------------------------
# Archivo: gui.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Perla Velasco & Yonathan Mtz.
# Version: 1.2 Abril 2017
# Descripción:
#
#   Este archivo define la interfaz gráfica del usuario. Recibe dos parámetros que posteriormente son enviados
#   a servicios que la interfaz utiliza.
#   
#   
#
#                                             gui.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Porporcionar la in-  | - Consume servicios    |
#           |          GUI          |    terfaz gráfica con la|   para proporcionar    |
#           |                       |    que el usuario hará  |   información al       |
#           |                       |    uso del sistema.     |   usuario.             |
#           +-----------------------+-------------------------+------------------------+
#
import os
from flask import Flask, render_template, request
import urllib, json
import requests
app = Flask (__name__)

@app.route("/")
def index():
	# Método que muestra el index del GUI
	return render_template("index.html")

@app.route("/information", methods=['GET'])
def sentiment_analysis():
	# Se obtienen los parámetros que nos permitirán realizar la consulta
	title = request.args.get("t")
	url_omdb = urllib.urlopen("http://localhost:8084/api/v1/information?t=" + title)
	# Se lee la respuesta de OMDB
	url_omdb_comentars=urllib.urlopen("http://localhost:8086/api/v1/comentarios?t=" + title)
	#Se lee la respuesta de los comentarios de twitter los lee y los manda a analizar
	json_omdb = url_omdb.read()
	json_comment=json.dumps(json.loads(url_omdb_comentars.read()))
	json_analisis=requests.post('http://localhost:8087/api/v1/analisisSent', json=json_comment)
	#Se guarda el json recibido con los comentarios analizados

	# Se convierte en un JSON la respuesta leída
	json_comentars=json.dumps(json.loads(json_analisis.text))
	omdb = json.loads(json_omdb)
	# Se llena el JSON que se enviará a la interfaz gráfica para mostrársela al usuario
	analisis_comentars= json.loads(json_comentars)
	# Se llena el JSON que se enviará a la interfaz gráfica para mostrársela al usuario
	json_result = {}
	json_result['omdb'] = omdb
	json_result['omdb_comentars']=analisis_comentars
	
	# Se regresa el template de la interfaz gráfica predefinido así como los datos que deberá cargar
	return render_template("status.html", result=json_result)
	

if __name__ == '__main__':
	# Se define el puerto del sistema operativo que utilizará el Sistema de Procesamiento de Comentarios (SPC).
	port = int(os.environ.get('PORT', 8000))
	# Se habilita el modo debug para visualizar errores
	app.debug = True
	# Se ejecuta el GUI con un host definido cómo '0.0.0.0' para que pueda ser accedido desde cualquier IP
	app.run(host='0.0.0.0', port=port)
