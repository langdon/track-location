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
<div id="map_canvas" style="width:640px;height:480px"></div>
<script type="text/javascript">
        $(function() {
                var yourStartLatLng = new google.maps.LatLng(42.333796,-71.051582);
                $('#map_canvas').gmap({'center': yourStartLatLng});
                % for row in data_grid:
                    % if loop.index < 20:
                $('#map_canvas').gmap('addMarker', { /*id:'m_${loop.index}',*/ 'position': '${row[1]},${row[2]}', 'bounds': true } ).click(function() {
                    $('#map_canvas').gmap('openInfoWindow', { 'content': 'time: ${row[3].strftime("%d/%m/%y %H:%M")}' }, this)});
                    % endif
               % endfor
        }); 
</script>
</div>
<p /> 
<div id="track-locations-grid">
    <table>
        <tr><th>id</th><th>lat</th><th>long</th><th>time</th></tr>
        % for row in data_grid:
        <tr><td>${row[0]}</td><td>${row[1]}</td><td>${row[2]}</td><td>${row[3].strftime("%d/%m/%y %H:%M")}</td></tr>
       % endfor
    </table>
</div>
</%block>
