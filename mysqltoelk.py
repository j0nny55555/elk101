#!/usr/bin/env python
# Anonymous Author & Jim McKibben
# 2018-04-05
"""Python2 code to import a MySQL Query to an ELK environment."""
import ipaddress, netaddr
from datetime import datetime
import MySQLdb
import MySQLdb.cursors
from pprint import pprint
debug = 0
#elastic stuffs
import requests
import json
from elasticsearch import Elasticsearch
url = '127.0.0.1'
es = Elasticsearch([{'host': url, 'port': 9200}])
mapping = '''
{
  "mappings":{
    "elementresearch":{
      "properties":{
        "date":{
          "type":"date",
          "format":"strict_date_optional_time||epoch_millis"
        }
        "srcip":{
          "type":"ip"
        }
        "dstip":{
          "type":"ip"
        }
      }
    }
  }
}'''

if es.indices.exists('elementresearch'):
  es.indices.delete(index='elementresearch')

es.indices.create(index='elementresearch', ignore=400, body=mapping)

import logging
logging.basicConfig(filename='mysqltoelkprocess.log',level=logging.WARNING,format='%(asctime)s %(message)s')
logging.warning('Started')
es_log = logging.getLogger("elasticsearch")
es_log.setLevel(logging.CRITICAL)

# sql garbage:
query = '''
    select 
 
    from 

    where 

    group by 

    order by 

'''
if debug: query = query + ' limit 1'
db = MySQLdb.connect(host="127.0.0.1",
	user="mysqluser",
	passwd="mysqlpass",
	db="mysqldb")
cur = db.cursor()
cur.execute(query)
logging.warning('Query ran, returned ' + str(cur.rowcount) + ' items. Starting http insert...')
e = {} #main dictionary
i = 1
for row in cur.fetchall(): # loop through each event returned
	element_id = int(row[4])
	e[element_id] = {} #start nesting
	time_date = int(row[18].strftime('%s')) * 1000
	e[element_id]['date'] = str(time_date)
	e[element_id]['element_number'] = int(row[3])
	e[element_id]['element_message'] = row[4]	
	if debug == 0:
		#print('Inserting event ' + str(i) + ', ' + row[12] + ', ' + row[10])
		es.index(index='elementresearch', doc_type='elements', id=element_id, body=json.dumps(e[element_id])) 
	else:
		print('RAW DICT: ')
		pprint(e[element_id])
		print('RAW JSON: ')
		pprint(json.dumps(e[element_id]))
	i += 1
db.close()
#pprint(e)
logging.warning('Complete!')
