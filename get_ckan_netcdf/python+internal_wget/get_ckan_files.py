#!/usr/bin/env python
# encoding: utf-8

#############################################
# Autori:   A.D'Ambrosio (ARPAC)
#           G.Bonafe' (ARPA-FVG)
# Utilizzo: Download files da CKAN ARPAE
# Progetto: ASI-ISPRA-QA
# Versione Python: 2
# Versioni script: 
#  data        autore  descrizione
#  2019-01-09  ADAm    prima versione
#  2019-03-29  GBon    credenziali esterne
#  2019-04-01  GBon    wget evita interruzioni
############################################

import urllib2
import json
import base64
import os
import argparse
import logging
import sys

# configura logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# argomenti
parser = argparse.ArgumentParser(description='Download from CKAN')
parser.add_argument('simulation', help='simulation', choices=['meteo', 'qa'])
parser.add_argument('domain', help='domain', choices=['centrosud', 'nord'])
parser.add_argument('type', help='type', choices=['latest', 'older'])
parser.add_argument('--locdir', default='./',          help='local download directory (default:./)')
parser.add_argument('--json',   default='./ckan.json', help='JSON with host, username, password (default:./ckan.json)')
args = parser.parse_args()

# legge credenziali dal JSON
# NB va predisposto sulla base del TEMPLATE
json_file = open(args.json, 'r')
ckan_config = json.load(json_file)
    
username = json.dumps(ckan_config["username"]).strip('"')
password = json.dumps(ckan_config["password"]).strip('"')
host =     json.dumps(ckan_config["host"]).strip('"')
address = 'https://' + host
package =   args.simulation + '-' + args.domain
if args.type == 'older':
  package = package + '-storico'
local_dir = args.locdir

#Preparazione richiesta del package desiderato
request = urllib2.Request(address + '/api/3/action/package_show?id='+package)
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)

try:
    response = urllib2.urlopen(request)
except Exception as e:
    logging.error(e.message)
    sys.exit(1)

assert response.code == 200
data=response.read()

response_dict = json.loads(data)        # Creazione dizionario dal json
assert response_dict['success'] is True # Controllo che il messaggio sia valido
result=response_dict['result']          # Accesso alle risorse
num_resources = result['num_resources'] # Numero di risorse
resources=result['resources']           # Nome e url dei files

# Download files
for i in range(0,num_resources):
    remote_file=resources[i]

    # Preparazione richiesta del singolo file per il download
    file_name = remote_file['name']
    request = urllib2.Request(remote_file['url'])
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    try:
        r = urllib2.urlopen(request)
    except Exception as e:
        logging.error(e.message)
        sys.exit(2)

    # Download del file
    local_file = os.path.join(local_dir, file_name)
    try:
        wget_opts = ' --progress=bar --tries=0 --continue --server-response --timeout=0 --retry-connrefused'
        wget_orig = ' "https://' + username + ":" + password + "@" + remote_file['url'].replace('https://', '') + '"'
        wget_dest = ' --output-document=' + local_file
        os.system('wget ' + wget_opts + wget_orig + wget_dest)
        is_downloaded = True
    except Exception as e:
        is_downloaded = False
        logging.warning(e.message)

    if (is_downloaded):
        logging.info('Download del file '+ file_name + ' terminato.')
    else:
        logging.warning('Download del file ' + file_name + ' fallito.')

sys.exit(0)
