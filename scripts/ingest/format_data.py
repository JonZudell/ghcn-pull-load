#/usr/bin/python
import psycopg2
import os
import time
import gzip
import sys


def format_by_key(line, accepted_elements):
    variables = line.split(',')
    result = {}
    result['ID']      = variables[0]
    result['YEAR']    = int(variables[1][0:4])
    result['MONTH']   = int(variables[1][4:6])
    result['DAY']     = int(variables[1][6:8])
    result['ELEMENT'] = variables[2]
    result['VALUE']   = float(variables[3])
    
    result['M_FLAG']  = variables[4]
    result['Q_FLAG']  = variables[5]
    result['S_FLAG']  = variables[6]

    if variables[7].strip() != '':
        result['HOUR']    = int(variables[7][0:2])
        result['MINUTE']  = int(variables[7][2:4])
    else:
        result['HOUR']    = ''
        result['MINUTE']  = ''

    
    if result['ELEMENT'] in accepted_elements:
        return result
    else:
        return None

def create_csv_line(line):
    ordered_keys = ['ID','YEAR','MONTH','DAY','HOUR','MINUTE','ELEMENT','VALUE','M_FLAG','Q_FLAG','S_FLAG']
    result = ''
    for key in ordered_keys:
        result += str(line[key])
        if key == ordered_keys[-1]:
            result += '\n'
        else:
            result += ','
    return result
    
    
def get_accepted_elements():
    conn = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}'".format(os.environ['INGEST_HOST'],
                                                                                       os.environ['INGEST_DB'],
                                                                                       os.environ['INGEST_USER'],
                                                                                       os.environ['INGEST_PASS']))
    cursor = conn.cursor()
    cursor.execute('SELECT "ELEMENT" FROM "META"."ELEMENTS_DEFINITION"')
    result = cursor.fetchall()
    result = [ item[0] for item in result ]
    conn.close()
    return result

def load(given_file, target_file):
    result = []
    accepted_elements = get_accepted_elements()
    with gzip.open(given_file, 'r') as this_file, open(target_file, 'w+') as output_file:
        for line in this_file:
            formatted_line = format_by_key(line, accepted_elements)
            if formatted_line is not None:
                output_file.write(create_csv_line(formatted_line))


if __name__ == '__main__':
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    input_dir = os.environ['DATA_DROP'] + '/yearly/unformatted/'
    target = os.environ['DATA_DROP'] + '/yearly/formatted/'
    files = [ f for f in os.listdir(input_dir) if start < int(f.split('.')[0]) <= end ] 
    print 'BEGINNING META LOAD PROCEDURE'
    total = 0
    for item in files:
        print 'STARTING LOAD FOR {0}'.format(item)
        start = time.time()
        load(input_dir + item, target + '.'.join(item.split('.')[0:2]))
        end = time.time() - start
        total += time.time() - start
        print 'ENDING LOAD FOR {0} COMPLETED IN {1} TIME'.format(item, end)
    print 'ALL LOADS FINISHED IN {0} TIME'.format(total)
