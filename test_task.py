import os
import shutil
import sys
import requests
import gzip
import re


def copy_files(source, destination=os.getcwd()):
    if sys.platform == 'win32':
        os.system('xcopy {0} {1}'.format(source, destination))
        #shutil.copyfileobj(f_in, f_out) TODO: Check on Win 10
    else:
        shutil.copy(source, destination)


def unzip_file(local_file):
    unziped_name = '.'.join(local_file.split('.')[0:2])
    with gzip.open(local_file, 'rb') as f_in:
        with open(unziped_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out) #It's STREAM!!!! not a file

def zip_files():
    pass


def download_file(url):
    local_filename = url.split('/')[-1]
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    my_request = requests.get(url, stream=True, headers=headers)
    print('Request code: ', my_request.status_code)
    if my_request.status_code == 200:
        with open(local_filename, 'wb') as f:
            for chunk in my_request.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(type(local_filename))
        return local_filename
    return None


def read_file(local_file):
    with open(local_file, 'r') as f:
        for line in f:
            re.match()


def main(arg):
    if arg.startswith('http'):
        downloaded_file = download_file(arg)
        if downloaded_file == None:
            print('File not found!')
        else:
            print('File: {0} is downloaded!'.format(download_file))
    else:
        if not os.path.isfile(arg):
            copy_files(arg)
        local_filename = arg.split('/')[-1]
        print('File: copy {} created'.format(local_filename))
        unzip_file(local_filename)
        print('Function unzip Done')


if __name__ == '__main__':
    while True:
        command = str(input('Enter path to the file or URL: '))
        if command != 'exit':
            if command.endswith(('.txt', '.txt.gz')):
                main(command)
            else:
                print(command, 'is not *.txt or *.txt.gz file')
        else:
            sys.exit()
