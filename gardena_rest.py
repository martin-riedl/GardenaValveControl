#######################################################################
#
# Dr.-Ing. Martin Riedl (2016)
#
#######################################################################

import time
import RPi.GPIO as GPIO

from flask import Flask, render_template
from threading import Timer

app = Flask(__name__)

valves = {
  "Valve 1" : "closed"
}

def timeout():
    print("closing timeout")
    pure_close()
    pure_close()

def statusPage():
  templateData = {
    'valves' : valves
  }
  return render_template('template.html', **templateData)

@app.route("/")
def hello():
  return statusPage()

def pure_open():
  GPIO.output(open, GPIO.HIGH)
  time.sleep(0.5)
  GPIO.output(open, GPIO.LOW)
  valves["Valve 1"]="opened"


@app.route("/open")
def def_open():
  return p_open(lambda : Timer(5*60, timeout).start())

@app.route("/openinf")
def p_open(exec_timer=lambda : None):
  pure_open()
  exec_timer()
  return statusPage()

def pure_close():
  GPIO.output(close, GPIO.HIGH)
  time.sleep(0.150)
  GPIO.output(close, GPIO.LOW)
  valves["Valve 1"]="closed"

@app.route("/close")
def f_close():
  pure_close()
  return statusPage()

if __name__ == "__main__":
  print("Setup GPIO")
  GPIO.setmode(GPIO.BCM)

  # define GPIO ports variables to open/close the valve
  open=22
  close=23

  pins = [open,close] #on, off

  for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

  app.run(host="0.0.0.0", port="4999")

  print("Cleanup")
  GPIO.cleanup()

