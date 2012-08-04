import sys, os
import ConfigParser
import psycopg2
from bottle import get, post, route, run, HTTPError, debug, template, static_file, default_app

DATA_ROOT = os.environ.get('OPENSHIFT_DATA_DIR', '')
CONFIG_FILE = DATA_ROOT + '/config.conf'

@route('/name/<name>')
def nameindex(name='Stranger'):
    return '<strong>Hello, %s!</strong>' % name
 
@route('/')
def index():
    return '<strong>Hello World!</strong>'

def get_config():
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)
    return config    
    
def get_connection():
    #get a connection object
    
    config = get_config()
    
    #Define our connection string
    conn_string = "host='" + config.get("Postgres Creds", "host") + "' "
    conn_string += "port='" + config.get("Postgres Creds", "port") + "' "
    conn_string += "user='" + config.get("Postgres Creds", "user") + "' "
    conn_string += "password='" + config.get("Postgres Creds", "pass") + "' "
    conn_string += "dbname='" + config.get("Postgres Creds", "db_name") + "' "
 
    con = None
    try:
        # print the connection string we will use to connect
    	print "Connecting to database\n	->%s" % (conn_string)
     
    	# get a connection, if a connect cannot be made an exception will be raised here
    	con = psycopg2.connect(conn_string)
     
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
        sys.exit(1)
                
    finally:        
        if con:
            con.close()

def test_db_connection():
    con = get_connection()
    cur = con.cursor()
    print "Connected!\n"
    
    cur.execute('SELECT version()')          
    print ver    
    
    ver = cur.fetchone()

#@route('/track-location/')
@post('/track-location/')
def track_location():
    try:
        #collect the location and time from the user
        geoX = request.forms.get('geoX')
        geoY = request.forms.get('geoY')
        time = request.forms.get('time')
    except NameError:
        #ignore for now
        
    test_db_connection()
    
    config = get_config()
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
