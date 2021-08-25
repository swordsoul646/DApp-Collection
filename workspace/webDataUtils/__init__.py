# -*- coding: utf-8 -*-

import _thread
import json
import os
import socket
import ssl
import time
import urllib.parse
import urllib.request

socket.setdefaulttimeout(15)

context = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/62.0.3202.62 Safari/537.36'}

debug = True

path = ''


def log(_str):
    print('[WebDataUtils] %s' % _str)


def setDebug(_debug):
    global debug
    if _debug:
        debug = True
    else:
        debug = False
    log('Debug is set to ' + str(debug))


def setPath(_path):
    global path
    path = _path
    log('Workspace is set to ' + path)


def encodeParams(o):
    return urllib.parse.urlencode(o)


def getWebData(url):
    line = ''
    if debug:
        log(url)
    req = urllib.request.Request(url=url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=context) as response:
            line = str(response.read(), encoding='utf-8')
    except Exception as e:
        if debug:
            log(str(e))
        line = ''
    if debug:
        log(str(len(line)))
    return line


def readJSONFile(fname):
    full_path = path + fname
    if not full_path.endswith('.json'):
        full_path += '.json'
    f = open(full_path, 'r')
    line = f.read()
    o = json.loads(line)
    f.close()
    return o


def writeJSONFile(fname, o):
    log('Write file: ' + path + fname + '.json')
    f = open(path + fname + '.json', 'w')
    f.write(json.dumps(o))
    f.close()


def writeFile(fname, o):
    log('Write file: ' + path + fname + '.txt')
    f = open(path + fname + '.txt', 'w')
    f.write(str(o))
    f.close()


def checkFolder(_path):
    if not os.path.exists(path + _path):
        os.mkdir(path + _path)
        log('Make folder: ' + path + _path)


def checkFile(fname):
    return os.path.exists(path + fname + '.json')


def getFileList(_path):
    return os.listdir(path + _path)


def printTime(delay):
    while True:
        time.sleep(delay)
        log("-------- %s --------" % (time.ctime(time.time())))


def startTimer(delay):
    try:
        _thread.start_new_thread(printTime, (delay,))
    except Exception as e:
        raise e
