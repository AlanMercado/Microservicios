# -*- coding: utf-8 -*-
#!/usr/bin/env python
#----------------------------------------------------------------------------------------------------------------
# Archivo: AnalisisComent.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Alan, Luis, Johan & jorge.
# Version: 1 Mayo 2017
# Descripción:
#
#   Este archivo recibe comentarios que posteriormente analizará
#   ya analizados devuelve un json
#   se revisa que polaridad tiene el comentario y lo regresa, se utiliza una libreria llamada TextBlob para obtener la polaridad
#   
#
#                                             Destwitts.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Analizar comentarios | - Consume servicios    |
#           |Analisis de comentarios|    recibidos para ver   |   de librerias que se  |
#           |                       |    su polaridad.        |   utilizan para        |
#           |                       |                         |   analizar texto       |
#           +-----------------------+-------------------------+------------------------+
#
import os,sys
from flask import Flask, abort, render_template, request
import urllib, json
import re
from textblob import TextBlob

app = Flask (__name__)

@app.route("/api/v1/analisisSent", methods=['POST'])
def get_information():
	json_data = {}
	json_input=request.get_json(force=True)
	#se recibe un json a través del metodo post
	
	#manda a llamar la función de análisis de sentimientos
	polarity = get_tweets(json_input)
	#itero y guardo los comentarios positivos, posteriormente guardo el total
	ppolar = [polar for polar in polarity if polar['sentiment'] == 'positive']
	totalpos=len(ppolar)
	# porcentaje de twitts positivos
	posiporcen=100*len(ppolar)/len(polarity)
	# itero y guardo los comentarios negativos, posteriormente guardo el total
	npolar = [polar for polar in polarity if polar['sentiment'] == 'negative']
	#porcentaje de twitts negativos
	negaporcen=100*len(npolar)/len(polarity)
	totalneg=len(npolar)
	# itero y guardo los comentarios neutrales, posteriormente guardo el total
	neutporcen=100*(len(polarity) - len(npolar) - len(ppolar))/len(polarity)
	totalneu=len(polarity)-len(npolar)-len(ppolar)
	#comentarios totales
	#creo un json
	total=len(polarity)
	enviar_analisis={}
	enviar_analisis['positiveporc']=posiporcen
	enviar_analisis['negativeporc']=negaporcen
	enviar_analisis['neutralporc']=neutporcen
	enviar_analisis['positive']=totalpos
	enviar_analisis['negative']=totalneg
	enviar_analisis['neutral']=totalneu
	enviar_analisis['total']=total
	return json.dumps(enviar_analisis)

def get_tweet_sentiment( sentiment):
	analysis = TextBlob(sentiment)
	#Método de análisis de comentarios, utiliza la libreria textblob
	if analysis.sentiment.polarity > 0:
		return 'positive'
	elif analysis.sentiment.polarity == 0:
		return 'neutral'
	else:
		return 'negative'

def get_tweets(input_json):
	clasifica = []
	#Método que recorre el json con los twitts y manda a llamar el método de analisis de comentarios
	json_clasifica=json.loads(input_json)
	for r in json_clasifica:
		
		
		parsed_tweet = {}
		# se guardan los twitts
		parsed_tweet['text'] = r['text']
		
		# se mandan a llamar la api de análisis y se obtienen clasificados
		parsed_tweet['sentiment'] = get_tweet_sentiment(r['text'])
		# se agregan al almacén de los comentarios
		clasifica.append(parsed_tweet)
	return clasifica
		



if __name__ == '__main__':
	
	port = int(os.environ.get('PORT', 8087))
	
	app.debug = True
	
	app.run(host='0.0.0.0', port=port)

