#!/usr/bin/python

import cwiid 
import time 

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
 
#turn on led to show connected 

while 1:
  wm.led = 1
  time.sleep(0.2)
  wm.led = 2
  time.sleep(0.2)
  wm.led = 4
  time.sleep(0.2)
  wm.led = 8
  time.sleep(0.2)
  print wm.state['buttons']

