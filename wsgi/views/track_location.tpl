<%inherit file="layout.tpl"/>
<%block name="page_includes">
<style>
#feedback { font-size: 1.4em; }
#selectable .ui-selecting { background: #FECA40; }
#selectable .ui-selected { background: #F39814; color: white; }
#selectable { list-style-type: none; margin: 0; padding: 0; width: 60%; }
#selectable li { margin: 3px; padding: 0.4em; font-size: 1.4em; height: 18px; }
</style>
<script>
</script>
</%block>
<%block name="content">
<div id="track-locations-map">
<script type="text/javascript">
        $(function() {
                var yourStartLatLng = new google.maps.LatLng(59.3426606750, 18.0736160278);
                $('#map_canvas').gmap({'center': yourStartLatLng});
        });
</script>
<div>
<p />
<div id="track-locations-grid">
    <p> ${ data_grid.replace('\n', '<br />\n') } </p>
</div>
</%block>
