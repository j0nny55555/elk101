#!/usr/bin/env python2
# Jim McKibben
# 2018-04-05
"""Python2 code to import a CSV to an ELK environment."""

from __future__ import print_function
from pprint import pprint
import os
import sys
import csv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from elasticsearch import Elasticsearch
from datetime import datetime
import dateutil.parser
from pytz import timezone
import ConfigParser

# Start of main
try:
    config = ConfigParser.ConfigParser()
    config.read("config.txt")
    elasticuser = config.get("configuration","username")
    elasticpass = config.get("configuration","password")
except:
    print("No config.txt - please copy config.example to config.txt and set your elastic user & pass")
    print("No config.txt - config.txt is not tracked by the project, your SSO is safe")
    sys.exit(0)

es = Elasticsearch(
    ['127.0.0.1'],
    http_auth=(elasticuser, elasticpass),
    #scheme="https",
    #use_ssl=True,
    verify_certs=False,
    port=9200
)

# Set Index name
indexname = "seckcwipi"

# index settings
bodymapping = '''{
    "properties":{
        "location":{
            "type":"geo_point"
        }
    }
}'''

bodysettings='''{
    "number_of_shards": 1,
    "number_of_replicas": 0
}'''

#if es.indices.exists(str(indexname)):
#    es.indices.delete(index=str(indexname))

# ignore 400 cause by IndexAlreadyExistsException when creating an index
try:
    #es.indices.create(index=str(indexname), ignore=400, body=bodysettings)
    #es.indices.create(index=str(indexname), ignore=400)
    es.indices.put_mapping(index=str(indexname), doc_type='syslogwithgeo', body=bodymapping)
    print('Created indice: '+indexname)
    mappingset = es.indices.get_mapping(index=str(indexname))
    pprint(mappingset)
except:
    e1 = sys.exc_info()[0]
    e2 = sys.exc_info()[1]
    print("Error creating indices: "+str(e1))
    print("Detail: "+str(e2))