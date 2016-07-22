#!/usr/bin/python

import sys
import optparse
import requests
import os


total_posted = 0
invalid_idocs = 0
ENDPOINT = 'http://localhost:3131/api/v1/product'

def list_idocs_on_directory(directory):
    files = []
    for _file in os.listdir(directory):
        if (_file).endswith('.xml'):
            files.append(_file)
    return files

def read_idoc(idoc, directory):
    data = None
    with open(os.path.join(directory, idoc), 'r') as f:
        data = f.read()
    return data

def send_idocs(directory):
    global invalid_idocs
    global total_posted
    _url = ENDPOINT
    _headers = { 'Content-Type' : 'application/xml' }

    idocs = list_idocs_on_directory(directory)
    print 'found %d idocs on directory' % len(idocs)
    for _idoc in idocs:
        _body = read_idoc(_idoc, directory)
        if _body is None:
            invalid_idocs = invalid_idocs + 1
            print 'invalid idoc', _idoc
            continue
        # print 'sending request', _url, '\n', _body
        try:
            r = requests.post(_url, data=_body, headers=_headers)
            total_posted = total_posted + 1
        except:
            print 'something went wrong when sending request', sys.exc_info()[0]
            print 'exit program'
            break


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-d', '--directory', dest='directory',
        help='The directory where the idocs are located')
    options, args = parser.parse_args()
    directory = options.directory
    if directory == '':
        print 'can not process empty directory'
    else:
        print 'searching on directory', directory
        send_idocs(directory)
        print 'successfully sent %d file(s) and found %d invalid objects' % (total_posted, invalid_idocs)
