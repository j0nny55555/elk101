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

# Function to digest the log file
def csv_dict_list(csvlog_file):
    reader = csv.DictReader(open(csvlog_file, 'rb'))
    rownum = 0
    for row in reader:
        try:
            # TODO make a function to check the time stamp format and use the correct one
            # TODO the nativity of the time stamp should be verified and if it is not naive, it should not be enlightened
            # TODO further, the replace method below doesn't handle timezones correctly, UTC is safe, everything else isn't
            # for when time like - 09 Jan 2018 11:59:09 PM
            #row['Date'] = datetime.strptime(row['Date'], '%d %b %Y %I:%M:%S %p')
            # for when time like - 1/9/2018 9:50:24 AM
            #row['Date'] = datetime.strptime(row['Date'], '%m/%d/%Y %I:%M:%S %p')
            # for when time like - 03/18/2015 07:44:00 PM
            row['Date'] = datetime.strptime(row['Date'], '%m/%d/%Y %I:%M:%S %p')
            row['Updated On'] = datetime.strptime(row['Updated On'], '%m/%d/%Y %I:%M:%S %p')
            # for when time like - 2018-01-08T04:48:37
            #row['Date'] = datetime.strptime(row['Date'], '%Y-%m-%dT%H:%M:%S')
            
            if rownum == 0:
                # Currently the time stamp is 'naive'
                print('Naive - Date:')
                print(row['Date'].strftime("%Y-%m-%d %H:%M:%S %Z%z"))

            # Now we add the UTC timezone to our naive date time stamp
            row['Date'] = row['Date'].replace(tzinfo=timezone('UTC'))
            row['Updated On'] = row['Updated On'].replace(tzinfo=timezone('UTC'))

            if rownum == 0:
                # Print the modified time stamp
                print('UTC - Date:')
                print(row['Date'].strftime("%Y-%m-%d %H:%M:%S %Z%z"))
                # Show time stamp in local time format
                print('CDT - Date:')
                print(row['Date'].astimezone(timezone('America/Chicago')).strftime("%Y-%m-%d %H:%M:%S %Z%z"))
                print('-------------------------------')
            
            print('Index '+str(rownum)+' of '+str(totalrows), end="\r")
            row['Location'] = row['Latitude']+","+row['Longitude']
            if(row['Location']==","):
                row['Location']=""
            if rownum == 0:
                for rowname in row:
                    print("----")
                    print("Field name: "+rowname)
                    rowvalue = row[rowname]
                    if(isinstance(rowvalue, datetime)):
                        continue
                    print("Field value: "+rowvalue)
                    if(rowvalue.lstrip('+-').isdigit()):
                        rowvalueasfloat = float(rowvalue)
                        if(rowvalueasfloat < 4294967295):
                            print("Is an Integer")
                            row[rowname] = int(rowvalue)
                    elif(rowvalue.lstrip('+-').replace(".", "", 1).isdigit()):
                        print("Is a Float")
                        row[rowname] = float(rowvalue)
                    else:
                        print("Likely string")
            else:
                rowvalue = row[rowname]
                if(isinstance(rowvalue, datetime)):
                    continue
                if(rowvalue.lstrip('+-').isdigit()):
                    rowvalueasfloat = float(rowvalue)
                    if(rowvalueasfloat < 4294967295):
                        row[rowname] = int(rowvalue)
                elif(rowvalue.lstrip('+-').replace(".", "", 1).isdigit()):
                    row[rowname] = float(rowvalue)

            
        except:
            e1 = sys.exc_info()[0]
            e2 = sys.exc_info()[1]
            print("Error with date: "+str(e1))
            print("Detail: "+str(e2))
            print("Look for line 28-33 for details in changing the time stamp format")
            pprint(row)
            sys.exit(0)
        try:
            es.index(index=''+str(indexname), id=sys.argv[1]+str(rownum), doc_type='log', body=row)
        except:
            e1 = sys.exc_info()[0]
            e2 = sys.exc_info()[1]
            print("Error indexing data: "+str(e1))
            print("Detail: "+str(e2))
            pprint(row)
            sys.exit(0)
        rownum += 1

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

# Set Index name from the 1st argument element
try:
    indexname = sys.argv[1].lower()
    print("Starting import for index: "+indexname)
except:
    print("Nothing specified to import")
    print("Execute like:")
    print("python csvtoelk.py indexname folderpath")
    sys.exit(0)
# The 2nd argument element is going to be the directory to work out of
for filename in os.listdir(sys.argv[2]):
    if filename.lower().endswith('.csv'):
        fullfilename = sys.argv[2]+filename
        print("Going to work on file: "+fullfilename)

        indexappend = filename.lower()
        print("Index append: "+indexappend)

        # Set index name to be indexname + attribute from file
        indexname+=indexappend
        totalrows = 0

        with open(fullfilename, 'rb') as checkcsvfile:
            checkcsvobject = csv.reader(checkcsvfile, delimiter=' ', quotechar='|')
            totalrows = sum(1 for row in checkcsvobject)
        print("Totals rows: "+str(totalrows))
    else:
        print("Skipping non CSV file: "+filename)
        continue

    # index settings
    bodymapping = '''{
        "properties":{
            "Arrest":{
                "type":"boolean"
            },
            "Beat":{
                "type":"integer"
            },
            "Community Area":{
                "type":"integer"
            },
            "Date":{
                "type":"date"
            },
            "District":{
                "type":"integer"
            },
            "ID":{
                "type":"integer"
            },
            "Location":{
                "type":"geo_point"
            },
            "Updated On":{
                "type":"date"
            },
            "Ward":{
                "type":"integer"
            },
            "X Coordinate":{
                "type":"integer"
            },
            "Y Coordinate":{
                "type":"integer"
            },
            "Year":{
                "type":"integer"
            }
        }
    }'''
    bodysettings='''{
        "number_of_shards": 1,
        "number_of_replicas": 0
    }'''

    # if es.indices.exists('alertdaily'):
    #   es.indices.delete(index='alertdaily')

    # ignore 400 cause by IndexAlreadyExistsException when creating an index
    try:
        es.indices.create(index=str(indexname), ignore=400, body=bodysettings)
        es.indices.put_mapping(index=str(indexname), doc_type='log', body=bodymapping)
        print('Created indice: '+indexname)
        mappingset = es.indices.get_mapping(index=str(indexname))
        pprint(mappingset)
    except:
        e1 = sys.exc_info()[0]
        e2 = sys.exc_info()[1]
        print("Error creating indices: "+str(e1))
        print("Detail: "+str(e2))

    # Create mapping
    # 'Date' looks like '2018-01-13 00:58:38 UTC+0000'
    # So - 'yyyy-MM-dd HH-mm-ss zZ'
    # As an option - "format":"yyyy-MM-dd HH-mm-ss zZ"
    # es.indices.put_mapping(
    #     index=""+str(indexname),
    #     doc_type="logs",
    #     body={
    #         "properties": {  
    #             "Date": {  
    #                 "type":"date"
    #             }
    #         }
    #     }
    # )

    csv_dict_list(fullfilename)
