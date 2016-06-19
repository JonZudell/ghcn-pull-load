#/usr/bin/python
import psycopg2
import os
import time
import sys

def load_file(loadable, cur, cols):
    this_file = open(loadable,'r')

    cur.copy_from(this_file, '"GHCN_DATA"."GHCN_GRANULAR"', sep=',', null='', columns=cols)

def run(start,end,conn):
    files_dir = os.environ['DATA_DROP'] + '/yearly/formatted/'
    files = [ f for f in os.listdir(files_dir) if start < int(f.split('.')[0]) <= end ]

    cols= ('"ID"','"YEAR"','"MONTH"','"DAY"','"HOUR"','"MINUTE"','"ELEMENT"','"VALUE"','"M_FLAG"','"Q_FLAG"','"S_FLAG"')
    total = 0
    cur = conn.cursor()
    print 'BEGINNING LOAD GHCN DATA PROCEDURE'
    for loadable in files:
        print 'LOADING {0}'.format(loadable)
        start = time.time()
        load_file(files_dir + loadable,cur, cols)
        end = time.time() - start
        total += end
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