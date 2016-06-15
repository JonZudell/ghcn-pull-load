#/usr/bin/python
import os
import psycopg2
import ingest.pull_meta
import ingest.load_meta
import ingest.pull_data
import ingest.load_data
#CREATE TABLES
def create_tables(files_location,cur):
    scripts = ['create_ghcn_data.sql','create_ghcn_data_ghcn_granular.sql','create_meta_data.sql',
	           'create_meta_data_country.sql','create_meta_data_elements_definition.sql','create_meta_data_inventory.sql',
			   'create_meta_data_state.sql','create_meta_data_stations.sql']
    for script in scripts:
        print "RUNNING {0}".format(script)
        cur.execute(open(files_location + '/' + script, "r").read())
#DOWNLOAD DATA
def load_elements_definition(file_location,cur):
    cur.execute(open(file_location + '/load_meta_data_elements_definition.sql', "r").read())
#FORMAT DATA
#PUSH DATA
#CREATE CONSTRAINTS AND INDEXES
if __name__ == '__main__':
    conn = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}'".format(os.environ['INGEST_HOST'],
	                                                                                   os.environ['INGEST_DB'],
																					   os.environ['INGEST_USER'],
																					   os.environ['INGEST_PASS']))
    cur = conn.cursor()
    create_tables(r'C:\Users\Jonathon\Desktop\ghcn-pull-load\database\create',cur)
    load_elements_definition(r'C:\Users\Jonathon\Desktop\ghcn-pull-load\database\load',cur)
    conn.commit()
    ingest.pull_meta.run()
    ingest.load_meta.run(cur)
    conn.commit()
    ingest.pull_data.run()
    ingest.format_data.run(-9999, 9999)
    ingest.load_data.run(-9999, 9999, cur)
    conn.commit()
    conn.close()