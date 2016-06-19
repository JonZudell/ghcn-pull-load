#/usr/bin/python
import os
import time
from ftplib import FTP

def pull(url, target, drop_location):
    #Connect
    ftp = FTP(url)
    ftp.login()
    ftp.cwd(target)
    file_names = [ f for f in ftp.nlst() if f.endswith('.csv.gz') ]
    for file_name in file_names:
        drop_target = '{0}/{1}'.format(drop_location,file_name)
        file = open(drop_target, 'wb')
        start = time.time()
        print 'STARTING DOWNLOAD FOR {0}'.format(file_name)
        try:
            ftp.retrbinary("RETR %s" % file_name, file.write)
        except:
            raise Exception('Failed to download file')
        file.close()
        print 'FINISHED DOWNLOAD FOR {0} IN {1}'.format(file_name, time.time() - start)
    ftp.close()
	
def run():
    url = os.environ['DATA_TARGET']
    drop_location = os.environ['DATA_DROP'] + '/yearly/unformatted/'
    target = 'pub/data/ghcn/daily/by_year/'
    print 'Pulling yearly files from {0}/{1} and pushing to {2}'.format(url,target,drop_location)
    pull(url ,target, drop_location)
	
if __name__ == '__main__':
    run()