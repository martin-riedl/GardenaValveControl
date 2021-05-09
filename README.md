# GardenaValveControl

A simple control unit that allows to switch Gardena 9V Valves 

This project builds a controler (which serves as a substitute for e.g. the Gardena C14e) to interface up to two 9V-valves. It can be connected to a Raspberry Pi and integrated with OpenHAB or other home automation solutions via a REST based interface.

## Setup

For python2
```bash
sudo apt-get install python-dev python-rpi.gpio
python -m pip install -r requirements.txt
```

For python3
```bash
sudo apt-get install python3-dev python3-rpi.gpio
python3 -m pip install -r requirements.txt
```

## Autostart @ RasperryPi
For autostart add the following line to `/etc/rc.local`:
```bash
/bin/sleep 15 && screen -dmS Gardena bash -c "python /home/pi/GardenaValveCtrl/gardena_rest.py" &
```

## OpenHAB Item
In `/etc/openhab2/items/default.items` the watering service can be accessed by, e.g. adding the following line (which has to be adapted your specific configuration): 
```java
Switch Gardena "Gardena Bewässerung" (gOutside) [ "Switchable" ] { http=">[ON:GET:http://gardena.local/open] >[OFF:GET:http://kitchen.local:4999/close]" }
String Gardena_Status           "Gardena Status [%s]"           <flow>          (gOutside)                              { http="<[http://gardena.local/status:10000:JSONPATH($[0].status)]" }
```

With the upgrade to OpenHab3, the http1-Binding is deprecated. The HTTP Bindung V2 is used instead. The following has to be added to a things file: 
```java
Thing http:url:gardena "Gardena" [ baseURL="http://192.168.0.4:4999/", commandMethod="GET", refresh="2" ] {
        Channels:
                Type switch : switch [ commandExtension="%2$s",  onValue="open", offValue="close" ]
                Type string : status [ stateExtension="status", stateTransformation="JSONPATH:$[0].status" ]
}
```
The following has to be added to an items file:
```java
Switch Gardena                  "Gardena Bewässerung"           <faucet>        (gOutside)      [ "Switchable" ]        { channel="http:url:gardena:switch" }
String Gardena_Status           "Gardena Status [%s]"           <flow>          (gOutside)                              { channel="http:url:gardena:status" }
```


By using OpenHab together with the Hue Binding, also Amazon Alexa can be used to control the watering service. 



## Watering WebService Status Page

The status page either shows closed and allows to switch on 
>   <h3>Gardena Valve Status</h3>
>   <p>Valve 1 is currently closed (<a href="/open">turn on</a>)</p>

or shows opened and allows to switch off
>   <h3>Gardena Valve Status</h3>
>   <p>Valve 1 is currently opened (<a href="/open">turn off</a>)</p>
   
## Circuit Configuration/Layout
You can find further information on the project [@Fritzing](http://fritzing.org/projects/gardena-valve-control).
