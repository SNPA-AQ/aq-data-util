#!/usr/bin/env python
# encoding: utf-8

#############################################
# Autore: ARPAC - A.D'Ambrosio
# Data: 09.01.2019
# Utilizzo: Download files da CKAN ARPAE
# Progetto: ASI-ISPRA
# Versione Python: 2
############################################

import urllib2
import json
import base64
import os

# legge credenziali da ckan.json
# NB va predisposto nella cartella di lavoro, 
# sulla base del TEMPLATE
with open('ckan.json', 'r') as json_file:  
    ckan_config = json.load(json_file)
    
username = json.dumps(ckan_config["username"]).strip('"')
password = json.dumps(ckan_config["password"]).strip('"')

def get_ckan_files(package, directory, username=username, password=password):

    # Package può assumere uno dei seguenti valori:
    # 'meteo-centrosud'
    # 'meteo-centrosud-storico'
    # 'meteo-nord'
    # 'meteo-nord-storico'
    # 'qa-centrosud'
    # 'qa-centrosud-storico'
    # 'qa-nord'
    # 'qa-nord-storico'


    #Preparazione richiesta del package desiderato
    request = urllib2.Request('https://asi-ispra-qa.arpae.it/api/3/action/package_show?id='+package)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)

    try:
        response = urllib2.urlopen(request)
    except Exception, e:
        print(e.message)
        exit(1)

    assert response.code == 200
    data=response.read()

    # Creazione dizionario dal json
    response_dict = json.loads(data)

    # Controllo che il messaggio sia valido
    assert response_dict['success'] is True

    # Accesso alle risorse
    result=response_dict['result']

    # Numero di risorse
    num_resources = result['num_resources']

    # Nome e url dei files
    resources=result['resources']

    # Download files
    for i in range(0,num_resources):
        file=resources[i]

        # Preparazione richiesta del singolo file per il download
        file_name = file['name']
        request = urllib2.Request(file['url'])
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)

        try:
            r = urllib2.urlopen(request)
        except Exception, e:
            print(e.message)
            exit(1)

        # Download del file
        CHUNK = 16 * 1024
        try:
            f = open(os.path.join(directory, file_name), 'wb')
            is_downloaded = True
        except IOError, e:
            print(e.message)
            exit(1)
        else:
            with  f:
                while True:
                    try:
                        chunk = r.read(CHUNK)
                    except Exception, e:
                        is_downloaded = False
                        print(e.message)
                        break
                    if not chunk:
                        break
                    f.write(chunk)

        if (is_downloaded):
            print('Download del file '+ file_name + ' '+ 'terminato.')
        else:
            print('Download del file ' + file_name + ' ' + 'fallito.')


# Esempio d'uso
get_ckan_files('qa-centrosud', 'D:\sistemi_informativi')

