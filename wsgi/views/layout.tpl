<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<%! 
    import os 
    
    def get_path_to_static():
        return os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 'runtime/repo/wsgi/static')
%>
  <head>
    <link rel="stylesheet" href="${ get_path_to_static() }/css/overcast/jquery-ui-1.8.21.custom.css" type="text/css" media="all" />
    <script src="http://maps.google.com/maps/api/js?sensor=true" type="text/javascript"></script>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js" type="text/javascript"></script>
    <script src="http://code.jquery.com/mobile/1.0/jquery.mobile-1.0.min.js" type="text/javascript" ></script>
    <script src="${ get_path_to_static() }/scripts/ui/jquery.ui.map.js" type="text/javascript"></script>
    <title><%block name="page_title">Track Location</%block></title>
    <%block name="page_includes"/>
  </head>
  <body>
    <%block name="content"/>
  </body>
</html>
