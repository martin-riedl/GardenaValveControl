#######################################################################
#
# Dr.-Ing. Martin Riedl (2016)
#
#######################################################################

import time
import RPi.GPIO as GPIO

from flask import Flask, render_template
from threading import Timer
from flask import jsonify
from typing import Text
app = Flask(__name__)

valves_config = []

valves_status = []

def timeout(gpio_close):
  """Timeout function which prints the closing event and for robustness applies the closing function multiple times."""

  print("closing timeout")
  pure_close(gpio_close=gpio_close)
  pure_close(gpio_close=gpio_close)

def statusPage() -> Text:
  """Create the HTML status page of the valves.

  Returns:
      Text: The valve status page.
  """
  templateData = {
    'valves' : valves_status
  }
  return render_template('template.html', **templateData)

def pure_open(gpio_open):
  GPIO.output(gpio_open, GPIO.HIGH)
  time.sleep(0.5)
  GPIO.output(gpio_open, GPIO.LOW)
  valves_status[0]["status"]="opened"
  print(valves_status)

def pure_close(gpio_close : int):
  """Closes a valve.
  Args:
      gpio_close (int): The closing GPIO port of the desired valve.
  """
  GPIO.output(gpio_close, GPIO.HIGH)
  time.sleep(0.150)
  GPIO.output(gpio_close, GPIO.LOW)
  valves_status[0]["status"]="closed"
  print(valves_status)

@app.route("/")
def hello():
  """Simply show the status page of the valves."""
  return statusPage()

@app.route("/status")
def get_status():
  """Shows a JSON representation of the valves status."""
  return jsonify(valves_status)

@app.route("/open")
@app.route("/open/<idx>")
def def_open(idx=0):
  """Performs a timebound opening of a valve and returns the updated status page."""
  return p_open(idx, lambda gpio_close: Timer(5*60, timeout(gpio_close=gpio_close)).start())

@app.route("/openinf")
@app.route("/openinf/<idx>")
def p_open(idx=0, exec_timer=lambda gpio_close : None):
  """Performs a boundless opening of a valve and returns the updated status page."""
  if len(valves_config)>0:
    pure_open(gpio_open=valves_config[idx]["open"])
    exec_timer(gpio_close=valves_config[idx]["close"])

  return statusPage()

@app.route("/close")
@app.route("/close/<idx>")
def f_close(idx=0):
  """Closes of a valve and returns the updated status page."""
  if len(valves_config)>0:
    pure_close(gpio_close=valves_config[idx]["close"])

  return statusPage()

if __name__ == "__main__":
  print("Setup GPIO")
  GPIO.setmode(GPIO.BCM)


  valves_config.append({
    "open" : 22,
    "close" : 23
  })
  valves_status.append({
    "status" : "closed"
  })

  # determine all gpio pins used
  pins = [pin for pin in [list(valve_config.values()) for valve_config in valves_config]]
  print(pins)

  for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

  app.run(host="0.0.0.0", port="4999")

  print("Cleanup")
  GPIO.cleanup()

