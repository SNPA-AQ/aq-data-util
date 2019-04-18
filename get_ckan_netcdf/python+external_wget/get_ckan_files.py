#!/dati/usr/anaconda2/bin/python
#encoding: utf - 8

#############################################
# Autore: ARPAC - A.D'Ambrosio
# Data: 09.01.2019
# Utilizzo: Download files da CKAN ARPAE
# Progetto: ASI-ISPRA
# Versione Python: 2
##
# modificato  03/2019 (A.D.F.):
# produce un file  di bash (wget_ITA7.get) con
# i comandi wget direzionati nella sottocartella ncfiles 
############################################

import os
import urllib2
import json
import base64

# Preparazione richiesta netcdf qa-nord
request = urllib2.Request('https://asi-ispra-qa.arpae.it/api/3/action/package_show?id=qa-nord')
base64string = base64.encodestring('%s:%s' % ('asi-ispra', 'asi-1SPR4-password!!')).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)

try:
 response = urllib2.urlopen(request)
except Exception, e:
  print(e.message)
  exit(1)

assert response.code == 200
data = response.read()

# Creazione dizionario dal json
response_dict = json.loads(data)

# Controllo che il messaggio sia valido
assert response_dict['success'] is True

# Accesso alle risorse
result = response_dict['result']

# Numero di risorse
num_resources = result['num_resources']

# Nome e url dei files
resources = result['resources']

# Download files
f= open("wget_ITA7.get","w+")
f.write('#!/bin/bash\n')
for i in range(0, num_resources):
  file = resources[i]
  # Preparazione richiesta del singolo file per il download
  file_name = file['name']
  print file_name
  file_url = file['url']
  request = urllib2.Request(file_url)
  base64string = base64.encodestring('%s:%s' % ('asi-ispra', 'asi-1SPR4-password!!')).replace('\n', '')
  f.write('wget --header \'Authorization: Basic ')
  f.write(base64string)
  f.write('\'  ')
  f.write(file_url)
  f.write(' -P ncfiles\n')
  
# Preparazione richiesta grib meteo-nord
request = urllib2.Request('https://asi-ispra-qa.arpae.it/api/3/action/package_show?id=meteo-nord')
base64string = base64.encodestring('%s:%s' % ('asi-ispra', 'asi-1SPR4-password!!')).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)

try:
 response = urllib2.urlopen(request)
except Exception, e:
  print(e.message)
  exit(1)

assert response.code == 200
data = response.read()

# Creazione dizionario dal json
response_dict = json.loads(data)

# Controllo che il messaggio sia valido
assert response_dict['success'] is True

# Accesso alle risorse
result = response_dict['result']

# Numero di risorse
num_resources = result['num_resources']

# Nome e url dei files
resources = result['resources']

# Download files
for i in range(0, num_resources):
  file = resources[i]
  # Preparazione richiesta del singolo file per il download
  file_name = file['name']
  print file_name
  file_url = file['url']
  request = urllib2.Request(file_url)
  base64string = base64.encodestring('%s:%s' % ('asi-ispra', 'asi-1SPR4-password!!')).replace('\n', '')
  f.write('wget --header \'Authorization: Basic ')
  f.write(base64string)
  f.write('\'  ')
  f.write(file_url)
  f.write(' -P ncfiles\n')  

f.close()     
