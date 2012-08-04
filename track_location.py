import urllib
import json
from bottle import route, run, HTTPError, debug, template, static_file

_LOCAL_DATA_URL = 'http://localhost:8090/Data/{0}'
_LOCAL_STATION_DATA_URL = 'http://localhost:8090/stations'
_CODE_FULL_PATH = '/home/lwhite/Documents/aptana-python-wkspc/mbta-wake-me-up-32/src'

@route('/')
@route('/index')
@route('/index.html')
@route('/index.htm')
def index():
    return template('index')
    
    