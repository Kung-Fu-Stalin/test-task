import os
import shutil
import sys
import gzip
import re
import requests
from zipfile import ZipFile


def copy_files(source, destination=os.getcwd()):
    # check_path = os.path.isfile(source)
    # file_size = os.path.getsize(source)
    # if check_path:
    if sys.platform == 'win32':
        os.system('xcopy {0} {1}'.format(source, destination))
            # shutil.copyfileobj(source, destination) TODO: Check on Win 10
    else:
        shutil.copy(source, destination)


def create_write_file(word):
    files_names = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    first_symbol = word[0]
    file_name = first_symbol + '.txt'
    if not os.path.isfile(file_name):
        open(file_name, 'a').close()
    if first_symbol in files_names:
        with open(file_name, 'a') as f:
            f.write(word)


def unzip_file(local_file):
    unzip_name = '.'.join(local_file.split('.')[0:2])
    with gzip.open(local_file, 'rb') as f_in:
        with open(unzip_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)  # It's STREAM!!!! not a file
    return unzip_name


def zip_file(cwd=os.getcwd()):
    files_to_zip = list(filter(lambda x: re.search(r'^[a-z].txt$', x), os.listdir(cwd)))
    with ZipFile('dictionary.zip', 'w') as zip_archive:
        for file_name in files_to_zip:
            zip_archive.write(file_name)
    for zipped_file in files_to_zip:
        os.remove(cwd + '/' + zipped_file)


def download_file(url):
    try:
        local_filename = url.split('/')[-1]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        # file_size = requests.head(url).headers['Content-Length'] TODO: Downloading progress
        # print(file_size)
        my_request = requests.get(url, stream=True, headers=headers)
        print('Request code: ', my_request.status_code)
        if my_request.status_code == 200:
            with open(local_filename, 'wb') as f:
                for chunk in my_request.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return local_filename
        return False
    except requests.exceptions.ConnectionError:
        return False


def read_file(local_file):
    with open(local_file, 'r') as f:
        for line in f:
            if re.search(r'[a-zA-Z\s]', line[0]):
                create_write_file(line.replace(' ', '').lower())


def main():
    while True:
        try:
            arg = str(input('Enter path to the file or URL: '))
            local_filename = arg.split('/')[-1]
            if arg == 'exit':
                sys.exit()
            if not arg.endswith(('.txt', '.txt.gz')):
                print(local_filename, 'is not *.txt or *.txt.gz file')
            else:
                if arg.startswith('http'):
                    downloaded_file = download_file(arg)
                    if downloaded_file is False:
                        print('Bad request')
                        continue
                    else:
                        print('File: {0} is downloaded!'.format(download_file))
                elif '/' in arg:  # TODO: Add backslash from win32
                    if os.path.isfile(arg):
                        copy_files(arg)
                        print('File: copy {} created'.format(local_filename))
                if arg.endswith('.gz'):
                    local_filename = unzip_file(local_filename)
                    print('Function unzip Done')
                read_file(local_filename)
                zip_file()
                print('Done')
        except FileNotFoundError:
            print('File not found!')


if __name__ == '__main__':
    main()
