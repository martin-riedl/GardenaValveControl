#######################################################################
#
# Dr.-Ing. Martin Riedl (2016)
#
#######################################################################

import time
import RPi.GPIO as GPIO

from flask import Flask, render_template
app = Flask(__name__)

valves = {
  "Valve 1" : "closed"
}

def statusPage():
  templateData = {
    'valves' : valves
  }
  return render_template('template.html', **templateData)

@app.route("/")
def hello():
  return statusPage()

@app.route("/open")
def open(): 
  GPIO.output(open, GPIO.HIGH)
  time.sleep(0.5)
  GPIO.output(open, GPIO.LOW)
  valves["Valve 1"]="opened"
  return statusPage()

@app.route("/close")
def close():
  GPIO.output(close, GPIO.HIGH)
  time.sleep(0.150)
  GPIO.output(close, GPIO.LOW)
  valves["Valve 1"]="closed"
  return statusPage()

if __name__ == "__main__":
  print "Setup GPIO"
  GPIO.setmode(GPIO.BCM)

  # define GPIO ports variables to open/close the valve
  open=22
  close=23

  pins = [open,close] #on, off
  
  for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

  app.run(host="0.0.0.0", port="4999")

  print "Cleanup"
  GPIO.cleanup()

