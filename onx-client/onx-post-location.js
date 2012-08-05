// Initializing variables 

var messageText = "where?";
//var targetServer = "http://trackloc-rheldev.rhcloud.com/track-location?geoX=lat&geoY=lon&time=currTime";
var targetServer = "http://trackloc-rheldev.rhcloud.com/track-location/";

// End of variables initializing 

console.log('Started script: When anyone texts me \"' +  messageText + '\" post with my location');

//  Register callback on sms received event
device.messaging.on('smsReceived', function (sms) {
    if (sms.data.body.toLowerCase() === messageText.toLowerCase()) {
        // getting location from cell, which is accurate enough in this case, time interval is 100  milliseconds, to get immediate location sample
        var locListener = device.location.createListener('CELL', 100);
        locListener.on('changed', function (signal) {
            // stop listening to location changed events after getting the current location
            locListener.stop();

            var locationTrackerUrl = targetServer.replace(/lat/g, signal.location.latitude).replace(/lon/g, signal.location.longitude).replace(/currTime/g, d.getTime());

            var d = new Date();
            var notification = device.notifications.createNotification('Calling locationTrackerUrl: ' + locationTrackerUrl);
                device.ajax(
                {
                  url: locationTrackerUrl,
                  type: 'POST',
                  data {
                      'geoX', signal.location.latitude,
                      'geoY', signal.location.longitude,
                      'time', d.getTime()
                  }
                },
                function onSuccess(body, textStatus, response) {
                  console.info('successfully received http response!');
                  notification.content = 'successfully received http response!';
                  notification.show();
                },
                function onError(textStatus, response) {
                  var error = {};
                  error.message = textStatus;
                  error.statusCode = response.status;
                    console.error('error: ',error);
                });
        });
        locListener.start();
    }
});
console.log('Completed script: When anyone texts me \"' +  messageText + '\" post with my location');