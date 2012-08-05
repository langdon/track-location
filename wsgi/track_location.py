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

def pp(cursor, data=None, rowlens=0):
    d = cursor.description
    if not d:
        return "#### NO RESULTS ###"
    names = []
    lengths = []
    rules = []
    if not data:
        t = cursor.fetchall()
    for dd in d:    # iterate over description
        l = dd[1]
        if not l:
            l = 12             # or default arg ...
        l = max(l, len(dd[0])) # handle long names
        names.append(dd[0])
        lengths.append(l)
    for col in range(len(lengths)):
        if rowlens:
            rls = [len(str(row[col])) for row in data if row[col]]
            lengths[col] = max([lengths[col]]+rls)
        rules.append("-"*lengths[col])
    format = " ".join(["%%-%ss" % l for l in lengths])
    result = [format % tuple(names)]
    result.append(format % tuple(rules))
    for row in data:
        result.append(format % row)
    return "\n".join(result)

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

@route('/name/<name>')
def nameindex(name='Stranger'):
    return '<strong>Hello, %s!</strong>' % name
 
@route('/')
def index():
    return '<strong>Hello World!</strong>'

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
    sql = "INSERT INTO locations (lat, long, time) VALUES (%s, %s, %s)"
    cursor.execute(sql, (geoX, geoY, time))    
    con.commit()

@get('/track-location/')
def track_location():
    #print out the locations found
    con = get_connection()
    cursor = con.cursor() #cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM locations')
    
    out = pp(cursor)
    cursor.close()
    return out

# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 
    'runtime/repo/wsgi/views/')) 

application=default_app()
