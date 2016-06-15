#/usr/bin/python
import os
import time
from ftplib import FTP

def pull(url, target, file_names, drop_location):
    #Connect
    ftp = FTP(url)
    ftp.login()
    ftp.cwd(target)
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
    drop_location = os.environ['DATA_DROP'] + '/meta/'
    target = 'pub/data/ghcn/daily'
    file_names = ['ghcnd-states.txt','ghcnd-stations.txt', 'ghcnd-countries.txt','ghcnd-inventory.txt']
    print 'Pulling {0} files from {1}/{2} and pushing to {3}'.format(len(file_names),url,target,drop_location)
    pull(url ,target, file_names, drop_location)

if __name__ == '__main__':
    run()