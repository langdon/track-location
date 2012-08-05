// Initializing variables 

var messageText = "where?";
//var targetServer = "http://trackloc-rheldev.rhcloud.com/track-location?geoX=lat&geoY=lon&time=currTime";
var targetServer = "http://trackloc-rheldev.rhcloud.com/track-location/";

// End of variables initializing 

console.log('Started script: When anyone texts me \"' +  messageText + '\" post with my location');

 device.scheduler.setTimer({
      name: "sendLocationAlarm", 
      time: 0,
      interval: 10*1000*60, 
      exact: false },
      function () { device.notifications.createNotification('Hello world!').show(); });

 device.screen.on('off', function () 
       { device.scheduler.removeTimer("uniqueAlarmName"); });
       
// Initializing variables 
var targetServer = "http://trackloc-rheldev.rhcloud.com/track-location/use-get?geoX=lat&geoY=lon&time=currTime&who=myPhoneNum";
// End of variables initializing 
console.log('Started script: post loc');
console.log("it is updated again 4");

//  Register callback on sms received event
 device.scheduler.setTimer({
      name: "sendLocationAlarm", 
      time: 0,
      interval: 10*1000*60,
      exact: false },
      function () {
        console.log("Timer fired, now = " + (new Date()));
        // getting location from cell, which is accurate enough in this case, time interval is 100  milliseconds, to get immediate location sample
        var locListener = device.location.createListener('CELL', 100);
        locListener.on('changed', function (signal) {
            // stop listening to location changed events after getting the current location
            locListener.stop();
            
            var d = new Date();
            var locationTrackerUrl = targetServer.replace(/lat/g, signal.location.latitude)
                .replace(/lon/g, signal.location.longitude)
                .replace(/currTime/g, d.getTime())
                .replace(/myPhoneNum/g, "6179533605");
    
            console.log('Calling locationTrackerUrl: ' + locationTrackerUrl);
            device.ajax(
                {
                  url: locationTrackerUrl
                },
                function onSuccess(body, textStatus, response) {
                  console.info('successfully received http response from get call!');
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
);
console.log('Completed script: post loc');