#!/usr/bin/python

import sys
import cwiid 
import threading
import time 
import RPi.GPIO as GPIO

connectionLost = 0

def SetupIO():
    print "Setup Raspberry PI GPIO for MSX joystick interface"
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(26, GPIO.OUT)

def alivePoll(wm):
    global connectionLost
    connectionLost = 0
    try:
        while 1:
            time.sleep(3)
            stat = wm.request_status()
    except RuntimeError: 
        pass
    connectionLost = 1
    wm.close()
    print "Connection lost"

def poll(wm):
    print "Polling Wiimote..."
    global connectionLost
    while not connectionLost:
        time.sleep(0.02)
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

def ConnectWiimote():
    print "Press 1+2 on your Wiimote now..."
    wm = None 
    while not wm: 
        try: 
            wm = cwiid.Wiimote() 
        except RuntimeError: 
            pass
    #set Wiimote to report button presses and accelerometer state 
    wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC 
    wm.led = 1
    return wm

def ProxyWiimoteToMSX():
    wiimote = ConnectWiimote()
    
    t = threading.Thread(target=alivePoll, args = [wiimote]) 
    t.daemon = True
    t.start()    
    
    poll(wiimote)  
    wiimote.close()

def MainLoop():
    try:
        ProxyWiimoteToMSX()
    except KeyboardInterrupt:
        print "keyboard exception..."
    except: 
        print "some unexcepted exception occurred..."
    
def main(argv):
    print "WiiMote 4 MSX host v1.0"
    print "Using RPi GPIO version " + GPIO.VERSION

    SetupIO()
    MainLoop()
    print "Shutting down normally"
    GPIO.cleanup();
    quit()
    
if __name__ == "__main__":
    main(sys.argv)
       

# testcode below, normally not executed...

while 0:
  GPIO.output(16, GPIO.HIGH)
  time.sleep(0.000001)
  GPIO.output(16, GPIO.LOW)
  time.sleep(0.000001)


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

#t2 = threading.Thread(target=poll) 
#t2.daemon = True
#t2.start()

try:
  while running:
    time.sleep(400)
except KeyboardInterrupt:
  print "stop..."
  quit()

print "exit..."
