#/usr/bin/python
import psycopg2
import os
import time
import gzip

queries = {'GHCN_DATA.GHCN_GRANULAR' : '''INSERT INTO "GHCN_DATA"."GHCN_GRANULAR"("ID","YEAR","MONTH","DAY","ELEMENT","VALUE","M_FLAG","Q_FLAG","S_FLAG","HOUR","MINUTE")
                                          VALUES(%(ID)s,%(YEAR)s,%(MONTH)s,%(DAY)s,%(ELEMENT)s,%(VALUE)s,%(M_FLAG)s,%(Q_FLAG)s,%(S_FLAG)s,%(HOUR)s,%(MINUTE)s)'''}

def format_by_key(line, accepted_elements):
    variables = line.split(',')
    result = {}
    result['ID']      = variables[0]
    result['YEAR']    = int(variables[1][0:4])
    result['MONTH']   = int(variables[1][4:6])
    result['DAY']     = int(variables[1][6:8])
    result['ELEMENT'] = variables[2]
    result['VALUE']   = float(variables[3])
    
    result['M_FLAG']  = variables[4] if variables[4] != '' else None
    result['Q_FLAG']  = variables[5] if variables[5] != '' else None
    result['S_FLAG']  = variables[6] if variables[6] != '' else None

    if variables[7].strip() != '':
        result['HOUR']    = int(variables[7][0:2])
        result['MINUTE']  = int(variables[7][2:4])
    else:
        result['HOUR']    = None
        result['MINUTE']  = None

    
    if result['ELEMENT'] in accepted_elements:
        return result
    else:
        return None


def insert(result, table, cursor):
    query = queries[table]
    cursor.executemany(query,result)
    
def get_accepted_elements(cursor):
    cursor.execute('SELECT "ELEMENT" FROM "META"."ELEMENTS_DEFINITION"')
    result = cursor.fetchall()
    result = [ item[0] for item in result ]
    return result

def load(given_file):
    conn = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}'".format(os.environ['INGEST_HOST'],
                                                                                       os.environ['INGEST_DB'],
                                                                                       os.environ['INGEST_USER'],
                                                                                       os.environ['INGEST_PASS']))
    cursor = conn.cursor()
    result = []
    accepted_elements = get_accepted_elements(cursor)
    with gzip.open(given_file, 'r') as this_file:
        for line in this_file:
            formatted_line = format_by_key(line, accepted_elements)
            if formatted_line is not None:
                result.append(formatted_line)

    insert(result, 'GHCN_DATA.GHCN_GRANULAR', cursor)
    conn.commit()
    cursor.close()

if __name__ == '__main__':
    directory = os.environ['DATA_DROP'] + '/yearly/'
    files = [ directory + '/' + f for f in os.listdir(directory) ] 
        
    print 'BEGINNING META LOAD PROCEDURE'
    total = 0
    for item in files:
        print 'STARTING LOAD FOR {0}'.format(item)
        start = time.time()
        load(item)
        end = time.time() - start
        total += time.time() - start
        print 'ENDING LOAD FOR {0} COMPLETED IN {1} TIME'.format(item, end)
    print 'ALL LOADS FINISHED IN {0} TIME'.format(total)
