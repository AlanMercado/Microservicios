# -*- coding: utf-8 -*-
#!/usr/bin/env python
#----------------------------------------------------------------------------------------------------------------
# Archivo: DesTwitts.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Alan, Luis, Johan & jorge.
# Version: 1 Mayo 2017
# Descripción:
#
#   Este archivo obtiene comentarios de una película y posteriormente los manda a clasificar
#   cuando los obtiene manda un json a la clase gui.py
#   
#   
#
#                                             DesTwitts.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Descargar comentarios| - Consume servicios    |
#           | Descargar Twitts.     |    de la red social     |   para proporcionar    |
#           |                       |    Twitter y guardarlos.|   información al       |
#           |                       |                         |   usuario.             |
#           +-----------------------+-------------------------+------------------------+
#
import os,sys
from flask import Flask, abort, render_template, request
import urllib, json
import re
import tweepy
from tweepy import OAuthHandler

app = Flask (__name__)
@app.route("/api/v1/comentarios")
def get_information():
	title = request.args.get("t")
	#Se revisa que se pasara un parámetro
	if title is not None:
		api = TwitterClient()
		#Se crea una variable de la clase TwitterClient()
        #Se descargan los tweets con un maximo de 200 comentarios y también se le pasa el título de la película
		tweets = api.get_tweets(query = title, count = 200)     
        for i in [0, 1, 2]:
        	print()
		#Se regresa el json
		return json.dumps(tweets)
	else:
		
		abort(400)

class TwitterClient(object):
    #Clase genérica de Twiitter para la descarga de comentarios
    def __init__(self):
        #Inicializador de la clase
        # llaves y tokens para el acceso a la api
        consumer_key = 'eg5wWIskWUrNfbkrvkeGde1aJ'
        consumer_secret = 's505yTRQcF2LOvCUCqP3gFJhglPCFSJlrbYbrdsmo2tc2zMMJq'
        access_token = '2173064522-0YlKXGga0xav1L5WGkvcyWmlGr5lUHuxnq5uEtd'
        access_token_secret = 'PGmnhZyeYzkv8KVWstosKuaTfPhfiQ9zij0x0z12j2BBK'
        # attempt authentication
        try:
            # creando objeto OAuthHandler
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # INgresando los tokens
            self.auth.set_access_token(access_token, access_token_secret)
            # creando un objeto tweepy API
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        #Es una funcion para limpiar los comentarios
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweets(self, query, count = 10):
        #Clase para obtener los twitt y la clasificacion de estos llamando a otra clase api.
        #Lista para los twitt y se le agrega el # para la pregunta y se le quitan los espacios para la consulta de los comentarios de peliculas
        tweets = []
        query="#"+query
        query=query.replace(" ","")

        try:
            #Llamada a la api de twitter
            fetched_tweets = self.api.search(q = query, count = count)
            #Abrimos un archivo de texto
            outfile = open('comentarios.txt', 'a') # Indicamos el valor 'a' que nos permite sobreescribir en un archivo de texto.
            for tweet in fetched_tweets:#recorremos los twitts 1 por 1
                parsed_tweet = {}

                parsed_tweet['text'] = self.clean_tweet(tweet.text)
                #Se guardan los  tanto en una variable como en archivo de texto
                outfile.write(self.clean_tweet(tweet.text)+'\n')
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
                

            #se cierra el archivo
            outfile.close()
            # regresa los twitts
            return tweets
 
        except tweepy.TweepError as e:
            # print error 
            print("Error : " + str(e))


if __name__ == '__main__':
	
	port = int(os.environ.get('PORT', 8086))
	
	app.debug = True
	
	app.run(host='0.0.0.0', port=port)