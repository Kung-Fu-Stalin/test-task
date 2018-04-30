import os
import shutil
import sys
import gzip
import re
import requests
from zipfile import ZipFile


FILE_NAMES = [chr(x) for x in range(ord('a'), ord('z') + 1)]


def remove_temp_files(is_archive, local_filename):
    if is_archive is True:
        os.remove(os.getcwd() + '/' + local_filename)


def copy_files(source):
    try:
        destination = os.getcwd()
        shutil.copy(source, destination)
    except shutil.SameFileError:
        print('[E] This file already exist in working directory!')


def create_write_file(word):
    first_symbol = word[0]
    file_name = first_symbol + '.txt'
    if not os.path.isfile(file_name):
        open(file_name, 'a').close()
    if first_symbol in FILE_NAMES:
        with open(file_name, 'a') as f:
            f.write(word)


def unzip_file(local_file):
    unzip_name = '.'.join(local_file.split('.')[0:2])
    with gzip.open(local_file, 'rb') as f_in:
        with open(unzip_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return unzip_name


def zip_file():
    cwd = os.getcwd()
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
        my_request = requests.get(url, stream=True, headers=headers)
        print('Request code: ', my_request.status_code)
        if my_request.status_code == 200:
            with open(local_filename, 'wb') as f:
                for chunk in my_request.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return local_filename
    except requests.exceptions.ConnectionError:
        pass
    return False


def read_file(local_file):
    with open(local_file, 'r') as f:
        for line in f:
            if re.search(r'[a-zA-Z\ ]', line[0]):
                create_write_file(line.replace(' ', '').lower())


def main():
    while True:
        try:
            command = str(input('Enter path to the file or URL: '))
            local_filename = command.split('/')[-1]
            if command == 'exit':
                sys.exit()
            if not command.endswith(('.txt', '.txt.gz')):
                print('[E]', local_filename, 'is not *.txt or *.txt.gz file')
            else:

                is_archive = False
                if command.startswith('http'):
                    downloaded_file = download_file(command)
                    if downloaded_file is False:
                        print('[E] Bad request')
                        continue
                    else:
                        print('File: {0} is downloaded!'.format(downloaded_file))
                elif '/' in command:
                    if os.path.isfile(command):
                        copy_files(command)
                        print('File: copy {} created'.format(local_filename))
                if command.endswith('.gz'):
                    is_archive = True
                    local_filename = unzip_file(local_filename)
                    print('Function unzip Done')
                read_file(local_filename)
                zip_file()
                remove_temp_files(is_archive, local_filename)
                print('Done')
        except FileNotFoundError:
            print('[E] File not found!')
        except UnicodeDecodeError:
            print('[E] Decode Error: file is not \'.txt\' or \'.txt.gz\', but have one of this file extension!')


if __name__ == '__main__':
    main()