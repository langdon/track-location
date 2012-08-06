import sys, os
import ConfigParser
import psycopg2
from pprint import pprint
from bottle import get, post, route, run, request, HTTPError, debug, static_file, default_app
from bottle import mako_view as view, mako_template as template
import json
import datetime

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
        data = cursor.fetchall()
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

def save_record(geoX, geoY, time, who):
    #save it in the db
    con = get_connection()
    cursor = con.cursor()
    sql = "INSERT INTO locations (lat, long, time, who) VALUES (%s, %s, %s, %s)"
    print "sql to insert: %s" % sql
    cursor.execute(sql, (geoX, geoY, time, who))    
    con.commit()

def get_path_to_static():
    return os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 'runtime/repo/wsgi/static')

@route('/name/<name>')
def nameindex(name='Stranger'):
    return '<strong>Hello, %s!</strong>' % name
 
@route('/')
def index():
    return '<strong>Hello World!</strong>'

@route('/css/<filepath:path>')
def server_css(filepath):
    return static_file(filepath, root= get_path_to_static() + '/css')

@route('/scripts/<filepath:path>')
def server_scripts(filepath):
    return static_file(filepath, root= get_path_to_static() + '/scripts')

#@route('/track-location/')
#@post('/track-location')
#@post('/track-location/')
@route('/track-location/', method='POST')
def track_location_post():
    try:
        #collect the location and time from the user
        #these should work per the bottlepy docs, not sure what is up
        #geoX = request.forms.geoX
        #geoY = request.forms.geoY
        #time = request.forms.time

        #these do
        geoX = request.get('HTTP_GEOX')
        geoY = request.get('HTTP_GEOY')
        time = request.get('HTTP_TIME')
        who = request.get('HTTP_WHO')
        
        print "got the following from the post: geoX=%s, geoY=%s, time=%s, who=%s" % (geoX, geoY, time, who)
    except NameError, e:
        #ignore for now
        print "form posted missing fields: %s" % e
        return "required fields missing"
    
    save_record(geoX, geoY, time, who)
    
@route('/track-location/use-get')
def track_location_get_for_post():
    try:
        #collect the location and time from the user
        #these should work per the bottlepy docs, not sure what is up
        geoX = request.query.geoX
        geoY = request.query.geoY
        time = datetime.datetime.fromtimestamp(int(request.query.time)/1000.0)
        who  = request.query.who

        #print "\n\n\n\n"
        #for x in request:
        #    print "request row: %s, type=%s" % (x, type(x))
        #print "\n\n\n\n"
 
        print "got the following from the post: geoX=%s, geoY=%s, time=%s, who=%s" % (geoX, geoY, time, who)
    except NameError, e:
        #ignore for now
        print "form posted missing fields: %s" % e
        return "required fields missing"
        
    save_record(geoX, geoY, time, who)

@get('/track-location')
@get('/track-location/')
def track_location_get():
    #print out the locations found
    con = get_connection()
    cursor = con.cursor() #cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM locations')
    
    table_rows_all = cursor.fetchall()
    table_rows_useful = []
    last_lat = 0.0
    last_long = 0.0
    for row in table_rows_all:
        row= (row[0], float(row[1]), float(row[2]), row[3], row[4])
        if ((last_lat != round(row[1], 2)) or (last_long != round(row[2], 2))):
            table_rows_useful.append(row)
        last_lat = round(row[1], 2)
        last_long = round(row[2], 2)

    cursor.close()
    return template('track_location', dict(data_grid=table_rows_useful ))

@get('/add-location')
@get('/add-location/')
def track_location_add_as_form():
    out = '''
        <html>
            <body>
                <form action="/track-location/">
                    geoX: <input type="text" name="geoX" /><br />
                    geoY: <input type="text" name="geoY" /><br />
                    time: <input type="text" name="time" /><br />
                    <input type="submit" value="Submit" />
                </form>
            </body>
        </html>
    '''
    return out

# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 
    'runtime/repo/wsgi/views/')) 

application=default_app()
