import sys, os
import ConfigParser
import psycopg2
from bottle import get, post, route, run, HTTPError, debug, template, static_file, default_app


@route('/name/<name>')
def nameindex(name='Stranger'):
    return '<strong>Hello, %s!</strong>' % name
 
@route('/')
def index():
    return '<strong>Hello World!</strong>'


@post('/track-location/')
def track_location():
    #collect the location and time from the user
    geoX = request.forms.get('geoX')
    geoY = request.forms.get('geoY')
    time = request.forms.get('time')

    config = ConfigParser.ConfigParser()
    config.read('config.conf')
    config.read(['site.cfg', os.path.expanduser('~/.myapp.cfg')])

    out = str(config.sections())
    out += str(config.get("Postgres Creds", "user"))
    return out
    #save it in the db

# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 
    'runtime/repo/wsgi/views/')) 

application=default_app()
