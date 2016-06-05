#/usr/bin/python
import os
from ftplib import FTP

def pull(url, target, file_names, drop_location):
    #Connect
    ftp = FTP(url)
    ftp.login()
    ftp.cwd(target)
    for file_name in file_names:
        drop_target = '{0}/{1}'.format(drop_location,file_name)
        file = open(drop_target, 'wb')
        try:
            ftp.retrbinary("RETR %s" % file_name, file.write)
        except:
            raise Exception('Failed to download file')
        file.close()
    ftp.close()

if __name__ == '__main__':
    url = os.environ['DATA_TARGET']
    drop_location = os.environ['DATA_DROP'] + '/daily/'
    target = 'pub/data/ghcn/daily'
    file_names = ['ghcnd_all.tar.gz']
    print 'Pulling {0} files from {1}/{2} and pushing to {3}'.format(len(file_names),url,target,drop_location)
    pull(url ,target, file_names, drop_location)
