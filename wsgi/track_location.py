import psycopg2
import sys
from bottle import route, default_app
from bottle import get, post, route, run, HTTPError, debug, template, static_file


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

    #save it in the db

    con = None

    try:
        con = psycopg2.connect(database='testdb', user='janbodnar') 
        cur = con.cursor()
        cur.execute('SELECT version()')          
        ver = cur.fetchone()
        print ver    
        
    
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
        sys.exit(1)
        
        
    finally:
        
        if con:
            con.close()
        

# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 
    'runtime/repo/wsgi/views/')) 

application=default_app()
