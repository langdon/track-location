<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <link rel="stylesheet" href="/css/overcast/jquery-ui-1.8.21.custom.css" type="text/css" media="all" />
  	<script src="/scripts/jquery-1.7.2.min.js" type="text/javascript" charset="utf-8"></script>
  	<script src="/scripts/jquery-ui-1.8.21.custom.min.js" type="text/javascript" charset="utf-8"></script>
  	<script src="/scripts/moment.js" type="text/javascript" charset="utf-8"></script>
    <script src="http://maps.google.com/maps/api/js?sensor=true" type="text/javascript"></script>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js" type="text/javascript"></script>
    <script src="http://code.jquery.com/mobile/1.0/jquery.mobile-1.0.min.js" type="text/javascript" ></script>
    <script src="{{ os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 'runtime/repo/wsgi/static/scripts') }}/ui/jquery.ui.map.full.min.js" type="text/javascript"></script>
    {{!get('page_includes', '')}}
  	<title>{{get('title', 'Track Location')}}</title>
  </head>
  <body>
	  %include
  </body>
</html>
