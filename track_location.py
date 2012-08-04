import psycopg2
import sys
from bottle import get, post, route, run, HTTPError, debug, template, static_file

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
        
        
    