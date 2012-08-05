import sys, os
import ConfigParser
import psycopg2
from bottle import get, post, route, run, request, HTTPError, debug, template, static_file, default_app

DATA_ROOT = os.environ.get('OPENSHIFT_DATA_DIR', '')
CONFIG_FILE = DATA_ROOT + '/config.conf'

_connection = None
 
def get_connection():
    #get a connection object

    global _connection
    if (_connection is None):
        print "no connection, creating"
        
        config = get_config()
        print "getting the connection string from the config file"
        
        #Define our connection string
        conn_string = "host='" + config.get("Postgres Creds", "host") + "' "
        conn_string += "port='" + config.get("Postgres Creds", "port") + "' "
        conn_string += "user='" + config.get("Postgres Creds", "user") + "' "
        conn_string += "dbname='" + config.get("Postgres Creds", "db_name") + "' "
     
        try:
            # print the connection string we will use to connect
            print "Connecting to database\n	->%s" % (conn_string)
            conn_string += "password='" + config.get("Postgres Creds", "pass") + "' "
         
        	# get a connection, if a connect cannot be made an exception will be raised here
            _connection = psycopg2.connect(conn_string)
         
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e    
            sys.exit(1)
        
        test_db_connection()
    
    print "returning connection, object is: %s" % _connection
    return _connection 

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
    
def test_db_connection():
    con = get_connection()
    
    cur = con.cursor()
    print "Testing Connected!\n"
    
    cur.execute('SELECT version()')          
    ver = cur.fetchone()
    print ver 
    cur.close()

#@route('/track-location/')
@post('/track-location/')
def track_location():
    try:
        #collect the location and time from the user
        geoX = request.forms.get('geoX')
        geoY = request.forms.get('geoY')
        time = request.forms.get('time')
    except NameError, e:
        #ignore for now
        print "form posted missing fields: %s" % e
        return "required fields missing"
        
    #save it in the db
    con = get_connection()
    cursor = con.cursor()
    sql = "INSERT INTO locations (lat, long, id, name, weight) VALUES (%s, %s, %s)"
    self.cursor.execute(sql, (item.id, item.title, item.order))
    cursor.execute('SELECT * FROM locations')
    
    out = ""
    for row in cursor:
        out += "%s    %s<br />\n" % row
    cursor.close()
    return out

@get('/track-location/')
def track_location():
    #print out the locations found
    con = get_connection()
    cursor = con.cursor() #cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM locations')
    
    out = ""
    for row in cursor:
        out += "%s    %s<br />\n" % row
    cursor.close()
    return out

# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 
    'runtime/repo/wsgi/views/')) 

application=default_app()
