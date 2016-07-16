#/usr/bin/python
import os
import psycopg2
import ingest.pull_meta
import ingest.load_meta
import ingest.pull_data
import ingest.load_data
import ingest.format_data
import ingest.generate_summaries
import time
#CREATE TABLES
def create_tables(files_location,conn):
    cur = conn.cursor()
    scripts = ['create_ghcn_data.sql', 'create_ghcn_data_ghcn_base.sql','create_ghcn_data_ghcn_summary.sql',
               'create_ghcn_data_ghcn_tmax.sql', 'create_ghcn_data_ghcn_tmin.sql',
               'create_ghcn_data_ghcn_awdr.sql','create_ghcn_data_ghcn_prcp.sql',
               'create_ghcn_data_ghcn_awnd.sql','create_ghcn_data_ghcn_tavg.sql',
               'create_ghcn_data_ghcn_snwd.sql','create_meta_data.sql',
               'create_ghcn_data_ghcn_wt.sql','create_ghcn_data_ghcn_tobs.sql',
               'create_meta_data_country.sql','create_meta_data_elements_definition.sql',
               'create_meta_data_inventory.sql','create_ghcn_data_ghcn_snow.sql',
               'create_meta_data_state.sql','create_meta_data_stations.sql']
    for script in scripts:
        print "RUNNING {0}".format(script)
        cur.execute(open(files_location + '/' + script, "r").read())
        conn.commit()


        
#DOWNLOAD DATA
def load_elements_definition(file_location,cur):
    cur.execute(open(file_location + '/load_meta_data_elements_definition.sql', "r").read())

#CREATE CONSTRAINTS AND INDEXES
if __name__ == '__main__':
    conn = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}'".format(os.environ['INGEST_HOST'],
                                                                                       os.environ['INGEST_DB'],
                                                                                       os.environ['INGEST_USER'],
                                                                                       os.environ['INGEST_PASS']))
    ghcn_dir = os.environ['GHCN_HOME']
    cur = conn.cursor()
    create_tables(ghcn_dir + '/database/create',conn)
    load_elements_definition(ghcn_dir + '/database/load',cur)
    conn.commit()
    ingest.pull_meta.run()
    ingest.load_meta.run(cur)
    conn.commit()
    ingest.pull_data.run()
    ingest.format_data.run(-9999, 9999, conn)
    ingest.load_data.run(-9999, 9999, conn)
    ingest.generate_summaries.run(conn)
    conn.commit()
    conn.close()
