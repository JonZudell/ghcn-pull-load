#/usr/bin/python
import psycopg2
import os
import time
import gzip
import sys
import subprocess
import cStringIO

#POTENTIALLY OPTIMIZE
def format_by_key(line, accepted_elements, wmo_stations):
    variables = line.split(',')
    result = {}
    result['ID']      = variables[0]
    result['YEAR']    = int(variables[1][0:4]) if variables[1][0:4] != '' else ''
    result['MONTH']   = int(variables[1][4:6]) if variables[1][4:6] != '' else ''
    result['DAY']     = int(variables[1][6:8]) if variables[1][6:8] != '' else ''
    result['ELEMENT'] = variables[2]
    result['VALUE']   = float(variables[3]) if variables[3] != '' else ''
    
    result['M_FLAG']  = variables[4]
    result['Q_FLAG']  = variables[5]
    result['S_FLAG']  = variables[6]

    if variables[7].strip() != '':
        result['HOUR']    = int(variables[7][0:2])
        result['MINUTE']  = int(variables[7][2:4])
    else:
        result['HOUR']    = ''
        result['MINUTE']  = ''
    
    if result['ELEMENT'] in accepted_elements and result['ID'] in wmo_stations:
        return result
    else:
        return None

def create_csv_line(line):
    ordered_keys = ['ID','YEAR','MONTH','DAY','HOUR','MINUTE','VALUE','M_FLAG','Q_FLAG','S_FLAG']
    result = ''
    for key in ordered_keys:
        result += str(line[key])
        if key == ordered_keys[-1]:
            result += '\n'
        else:
            result += ','
    return result

def get_wmo_stations(cursor):
    cursor.execute('''SELECT "ID" FROM "META"."STATIONS" WHERE "WMO_ID" <> '' ''')
    result = cursor.fetchall()
    result = [ item[0] for item in result ]
    return set(result)
    
    
def get_accepted_elements(cursor):
    cursor.execute('SELECT "ELEMENT" FROM "META"."ELEMENTS_DEFINITION"')
    result = cursor.fetchall()
    result = [ item[0] for item in result ]
    return set(result)

def yield_lines(given_file):
    sub_process = subprocess.Popen(["zcat", given_file], stdout = subprocess.PIPE)
    result_file = cStringIO.StringIO(sub_process.communicate()[0])
    for line in [line.rstrip('\n') for line in result_file]:
        yield line
    
#BATCH WRITE FORMATTED LINES
def format_files(given_file, target_file, accepted_elements, wmo_stations):
    lists_by_element = {}

    for line in yield_lines(given_file):
        formatted_line = format_by_key(line, accepted_elements, wmo_stations)
        if formatted_line is not None:
            if formatted_line['ELEMENT'] not in lists_by_element.keys():
                lists_by_element[formatted_line['ELEMENT']] = []
            lists_by_element[formatted_line['ELEMENT']].append(create_csv_line(formatted_line))
    
    for key in lists_by_element.keys():
        divided_target = target_file.split('.')[0] + '_' + key + '.' + target_file.split('.')[1]
        with open(divided_target, 'w+') as output_file:
            for line in lists_by_element[key]:
                output_file.write(line)
            
            
    #with open(target_file, 'w+') as output_file:
        #for line in yield_lines(given_file):
            #formatted_line = format_by_key(line, accepted_elements, wmo_stations)
            #if formatted_line is not None:
                #result.append(create_csv_line(formatted_line))
                #if len(result) > 9999:
                    #output_file.write(''.join(result))
                    #result = []
        #if len(result) > 0:
            #output_file.write(''.join(result))
    #os.remove(given_file)

def run(start, end, conn):
    input_dir = os.environ['DATA_DROP'] + '/yearly/unformatted/'
    target = os.environ['DATA_DROP'] + '/yearly/formatted/'
    files = [ f for f in os.listdir(input_dir) if start < int(f.split('.')[0]) <= end ]

    cursor = conn.cursor()
    accepted_elements = get_accepted_elements(cursor)
    wmo_stations = get_wmo_stations(cursor)

    print 'BEGINNING FORMAT GHCN DATA PROCEDURE'
    total = 0
    for item in files:
        print 'STARTING FORMAT FOR {0}'.format(item)
        start = time.time()
        format_files(input_dir + item, target + '.'.join(item.split('.')[0:2]), accepted_elements, wmo_stations)
        end = time.time() - start
        total += time.time() - start
        print 'ENDING FORMAT FOR {0} COMPLETED IN {1} TIME'.format(item, end)
    print 'ALL FORMATS FINISHED IN {0} TIME'.format(total)
	
if __name__ == '__main__':
    conn = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}'".format(os.environ['INGEST_HOST'],
                                                                                       os.environ['INGEST_DB'],
                                                                                       os.environ['INGEST_USER'],
                                                                                       os.environ['INGEST_PASS']))
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    run(start,end, conn)
    conn.close()
