# GardenaValveControl

A simple control unit that allows to switch Gardena 9V Valves 

This project builds a controler (which serves as a substitute for e.g. the Gardena C14e) to interface up to two 9V-valves. It can be connected to a Raspberry Pi and integrated with OpenHAB or other home automation solutions via a REST based interface.

## Autostart @ RasperryPi
For autostart add the following line to `/etc/rc.local`:
```bash
/bin/sleep 15 && screen -dmS Gardena bash -c "python /home/pi/GardenaValveCtrl/gardena_rest.py" &
```

## OpenHAB Item
In `/etc/openhab2/items/default.items` the watering service can be accessed by, e.g. adding the following line (which has to be adapted your specific configuration): 
```bash
Switch Gardena "Gardena Bewässerung" (gOutside) [ "Switchable" ] { http=">[ON:GET:http://kitchen.local:4999/open] >[OFF:GET:http://kitchen.local:4999/close]" }
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
