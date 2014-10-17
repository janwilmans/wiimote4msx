#!/usr/bin/python

import cwiid 
import threading
import time 
import RPi.GPIO as GPIO

running = 1

def signal():
  while 1:
    wm.led = 1
    time.sleep(2);
    wm.led = 2
    time.sleep(2);

def poll():
  while 1:
    buttons = wm.state['buttons']
    if (buttons & cwiid.BTN_1):
	print "Button 1"
        GPIO.output(13, GPIO.HIGH)
    else: 
        GPIO.output(13, GPIO.LOW)
    if (buttons & cwiid.BTN_2):
	print "Button 2"
        GPIO.output(19, GPIO.HIGH)
    else: 
        GPIO.output(19, GPIO.LOW)


    if (buttons & cwiid.BTN_RIGHT):
	print "Button U"
        GPIO.output(16, GPIO.HIGH)
    else: 
        GPIO.output(16, GPIO.LOW)

    if (buttons & cwiid.BTN_LEFT):
	print "Button D"
        GPIO.output(26, GPIO.HIGH)
    else: 
        GPIO.output(26, GPIO.LOW)

    if (buttons & cwiid.BTN_UP):
	print "Button L"
        GPIO.output(20, GPIO.HIGH)
    else: 
        GPIO.output(20, GPIO.LOW)

    if (buttons & cwiid.BTN_DOWN):
	print "Button R"
        GPIO.output(21, GPIO.HIGH)
    else: 
        GPIO.output(21, GPIO.LOW)


    if (buttons & cwiid.BTN_A):
	print "Button A"
    if (buttons & cwiid.BTN_B):
	print "Button B"
        global running
	running = 0
    time.sleep(0.05)


print "WiiMote 4 MSX host v1.0"
print "Using RPi GPIO version " + GPIO.VERSION

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

pin = 21

while 0:
  print "pin " + str(pin) + " = on"
  GPIO.output(pin, GPIO.HIGH)
  time.sleep(2)
  print "pin " + str(pin) + " = off"
  GPIO.output(pin, GPIO.LOW)
  time.sleep(2)



print 'Press 1+2 on your Wiimote now...' 
wm = None 
i=2 
while not wm: 
  try: 
    wm=cwiid.Wiimote() 
  except RuntimeError: 
    if (i>30): 
      print "no wiimote found after 30 scans..."
      quit() 
      break 
    i +=1 

#set Wiimote to report button presses and accelerometer state 
wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC 

t1 = threading.Thread(target=signal) 
t2 = threading.Thread(target=poll) 
t1.daemon = True
t2.daemon = True
t1.start()
t2.start()

try:
  while running:
    time.sleep(400)
except KeyboardInterrupt:
  print "stop..."
  quit()

print "exit..."
