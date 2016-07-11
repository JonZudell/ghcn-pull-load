#/usr/bin/python
import psycopg2
import os
import time
import sys

def load_file(loadable, file_type, cur, cols):
    this_file = open(loadable,'r')
    cur.copy_from(this_file, '"GHCN_DATA"."GHCN_{0}"'.format(file_type), sep=',', null='', columns=cols)

def run(start,end,conn):
    files_dir = os.environ['DATA_DROP'] + '/yearly/formatted/'

    cols= ('"ID"','"YEAR"','"MONTH"','"DAY"','"HOUR"','"MINUTE"',
           '"ELEMENT"','"VALUE"','"M_FLAG"','"Q_FLAG"','"S_FLAG"')
    total = 0
    cur = conn.cursor()

    print 'BEGINNING LOAD GHCN DATA PROCEDURE'
    file_types = ['PRCP', 'SNOW','SNWD', 'TMAX', 'TAVG', 'TMIN', 'AWND', 'AWDR', 'TOBS']
    files = [ f for f in os.listdir(files_dir) if start < int(f.split('.')[0].split('_')[0]) <= end]
    for loadable in files:
        print 'LOADING {0}'.format(loadable)
        start = time.time()
        file_type = None
        for f_type in file_types:
            if f_type in loadable:
                file_type = f_type

        if file_type is None:
            file_type = 'WT'

        load_file(files_dir + loadable, file_type, cur, cols)
            
        end = time.time() - start
        total += end
        os.remove(files_dir + loadable)
        print 'FINISHED LOAD FOR {0} in {1}'.format(loadable, end)
        conn.commit()
    cur.close()
    print 'FINISHED LOAD FOR {0} FILES in {1}'.format(len(files), total)

if __name__ == '__main__':
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    conn = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}'".format(os.environ['INGEST_HOST'],
	                                                                               os.environ['INGEST_DB'],
										       os.environ['INGEST_USER'],
										       os.environ['INGEST_PASS']))
    run(start,end,conn)
