#!/usr/bin/env python2
# Anonymous Author
# 2018-04-05
"""Python2 code to import a CSV to an ELK environment."""
import apiconn, ipaddress, netaddr, time, datetime
from pprint import pprint
import logging

#elastic stuffs
import requests
import json
from elasticsearch import Elasticsearch
url = '127.0.0.1'
es = Elasticsearch([{'host': url, 'port': 9200}])


debug = 1

user = ''
key = ''
url = 'https://domain.tld'
apiconn = thingapiversion.endpoint(user, key, url)

time_format = '%Y-%m-%dT%H:%M:%S.000Z' # HATE HATE HATE
elements = apiconn.enumerateThing()['result'] # grab all the list names and their properties

query_time = time.strftime(time_format)

print(query_time)
i=60

def es_insert(data):
	es.index(index='thing-totals', doc_type='element_totals', body=data)
while True:
	d = datetime.datetime.strptime(query_time, time_format) - datetime.timedelta(minutes=i)
	query_time = d.strftime(time_format)
	time.sleep(0.5)
	i+=60
	
	for item in elements: # loop over each list
		count = 1
		if item['type'] == 'OPTION1DONTCARE' or item['type'] == 'OPTION2DONTCARE':
			print('Skipping ' + item['displayName'])
		else:
			print('Inserting ' + item['displayName'] + ' from ' + query_time)
			try:
				if item['contentType'] == "OPTION3WEWANT":
					list_contents = apiconn.getgetElementsTime(item['name'], query_time)['result']['contents']
					for pattern in list_contents:
						count += 1
					es_insert({ 'element_id': item['id'], 'element_name': item['displayName'], 'element_revision': item['currentVersion'], 'element_type': item['contentType'], 'count': count, 'query_time': query_time })
				else:
					list_contents = apiconn.getElementsMetaTime(item['name'], query_time)['result']['contents']
					for pattern in list_contents:
						count += 1
					es_insert({ 'element_id': item['id'], 'elementname': item['displayName'], 'element_revision': item['currentVersion'], 'element_type': item['contentType'], 'count': count, 'query_time': query_time })
			except:
				print('error inserting ' +item['displayName'] + ' probably before creation!')
