#/usr/bin/python
import psycopg2
import os
import time

queries = {'META.STATES' : '''INSERT INTO "META"."STATES" ("CODE", "NAME") VALUES (%(CODE)s, %(NAME)s) ON CONFLICT DO NOTHING''',
           'META.COUNTRIES' : '''INSERT INTO "META"."COUNTRIES" ("CODE", "NAME") VALUES (%(CODE)s, %(NAME)s) ON CONFLICT DO NOTHING''',
           'META.STATIONS' : '''INSERT INTO "META"."STATIONS" ("ID", "LATITUDE", "LONGITUDE", "ELEVATION", "STATE", "NAME", "GSN_FLAG","HCN_CRN_FLAG", "WMO_ID") 
                                VALUES (%(ID)s, %(LATITUDE)s, %(LONGITUDE)s, %(ELEVATION)s, %(STATE)s, %(NAME)s, %(GSN_FLAG)s,%(HCN_CRN_FLAG)s, %(WMO_ID)s) ON CONFLICT DO NOTHING''',
           'META.INVENTORY' : '''INSERT INTO "META"."INVENTORY" ("ID", "LATITUDE", "LONGITUDE", "ELEMENT", "FIRSTYEAR", "LASTYEAR")
                                 VALUES (%(ID)s, %(LATITUDE)s, %(LONGITUDE)s, %(ELEMENT)s, %(FIRSTYEAR)s, %(LASTYEAR)s) ON CONFLICT DO NOTHING'''}

def format_by_key(line, keys):
    result = {}
    for key in keys:
        result[key['COLUMN_NAME']] = line[key['START']:key['END']].strip()
        if key['TYPE'] == 'real':
            result[key['COLUMN_NAME']] = float(result[key['COLUMN_NAME']])
        elif key['TYPE'] == 'int':
            result[key['COLUMN_NAME']] = int(result[key['COLUMN_NAME']])
    return result

def insert(result, table, cursor):
    query = queries[table]
    cursor.executemany(query,result)
    
def load(item):
    conn = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}'".format(os.environ['INGEST_HOST'],
                                                                                      os.environ['INGEST_DB'],
                                                                                      os.environ['INGEST_USER'],
                                                                                      os.environ['INGEST_PASS']))

    cursor = conn.cursor()
    result = []
    with open(item['LOCATION'], 'r') as  given_file:
        for line in given_file:
            result.append(format_by_key(line, item['KEYS']))
    insert(result, item['TABLE'], cursor)
    conn.commit()
    cursor.close()

if __name__ == '__main__':
    print 'BEGINNING META LOAD PROCEDURE'
    meta_location = os.environ['DATA_DROP'] + '/meta/'
    states_load = {'TABLE' : 'META.STATES',
                   'LOCATION' : meta_location + 'ghcnd-states.txt',
                   'KEYS' : [{'COLUMN_NAME' : 'CODE', 'START' : 0, 'END' : 2, 'TYPE' : 'str'},
                             {'COLUMN_NAME' : 'NAME', 'START' : 3, 'END' : 50, 'TYPE' : 'str'}]}
    
    countries_load = {'TABLE' : 'META.COUNTRIES', 
                      'LOCATION' : meta_location + 'ghcnd-countries.txt',
                      'KEYS' : [{'COLUMN_NAME' : 'CODE', 'START' : 0, 'END' : 2, 'TYPE' : 'str'},
                                {'COLUMN_NAME' : 'NAME', 'START' : 3, 'END' : 50, 'TYPE' : 'str'}]}
                                
    station_load = {'TABLE' : 'META.STATIONS',
                    'LOCATION' : meta_location + 'ghcnd-stations.txt',
                    'KEYS' : [{'COLUMN_NAME' : 'ID', 'START' : 0, 'END' : 11, 'TYPE' : 'str'},
                              {'COLUMN_NAME' : 'LATITUDE', 'START' : 12, 'END' : 20, 'TYPE' : 'real'},
                              {'COLUMN_NAME' : 'LONGITUDE', 'START' : 21, 'END' : 30, 'TYPE' : 'real'},
                              {'COLUMN_NAME' : 'ELEVATION', 'START' : 31, 'END' : 37, 'TYPE' : 'real'},
                              {'COLUMN_NAME' : 'STATE', 'START' : 38, 'END' : 40, 'TYPE' : 'str'},
                              {'COLUMN_NAME' : 'NAME', 'START' : 41, 'END' : 71, 'TYPE' : 'str'},
                              {'COLUMN_NAME' : 'GSN_FLAG', 'START' : 72, 'END' : 75, 'TYPE' : 'str'},
                              {'COLUMN_NAME' : 'HCN_CRN_FLAG', 'START' : 76, 'END' : 79, 'TYPE' : 'str'},
                              {'COLUMN_NAME' : 'WMO_ID', 'START' : 80, 'END' : 85, 'TYPE' : 'str'}]}

    inventory_load = {'TABLE' : 'META.INVENTORY',
                      'LOCATION' : meta_location + 'ghcnd-inventory.txt',
                      'KEYS' : [{'COLUMN_NAME' : 'ID', 'START' : 0, 'END' : 11, 'TYPE' : 'str'},
                                {'COLUMN_NAME' : 'LATITUDE', 'START' : 12, 'END' : 20, 'TYPE' : 'real'},
                                {'COLUMN_NAME' : 'LONGITUDE', 'START' : 21, 'END' : 30, 'TYPE' : 'real'},
                                {'COLUMN_NAME' : 'ELEMENT', 'START' : 31, 'END' : 35, 'TYPE' : 'str'},
                                {'COLUMN_NAME' : 'FIRSTYEAR', 'START' : 36, 'END' : 40, 'TYPE' : 'int'},
                                {'COLUMN_NAME' : 'LASTYEAR', 'START' : 41, 'END' : 455555, 'TYPE' : 'int'}]}
                                                                  
    loads = [states_load,countries_load,station_load,inventory_load]
    total = 0
    for item in loads:
        print 'STARTING LOAD FOR {0}'.format(item['TABLE'])
        start = time.time()
        load(item)
        end = time.time() - start
        total += time.time() - start
        print 'ENDING LOAD FOR {0} COMPLETED IN {1} TIME'.format(item['TABLE'], end)
    print 'ALL LOADS FINISHED IN {0} TIME'.format(total)
