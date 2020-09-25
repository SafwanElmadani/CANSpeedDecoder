#!/usr/bin/env python
import sys
import binascii
import time
import datetime
import csv
import numpy as np
import liveRadar as lt
import kalmanTracking as kt
import random
import threading

import rospy
from std_msgs.msg import String, UInt8
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Float64
from visualization_msgs.msg import Marker
from geometry_msgs.msg import TwistStamped

import threading, time, random
from playsound import playsound

#initializeing kalman filter object
df = 0.04
leader = kt.KF_Object([5,0],0, 0, df, 1,1,1)
#initializing ROS value variables
gnewLeadMeasurement = 1
gmyDetections = []
gnewVel=0.0
#initializing CAN Coach variables
velocity = 40
th = 3.14159
relv = 0
lead = 0
#initializing sound feedback variables
mode = 0
setPoint = 2.25
#thSet = 2
thBounds = 0.05
feedbackType = 1

#testing that sound works as things start up
soundpath = '/home/eternity/catkin_ws/src/can_to_ros/sounds/'
welcome1 = 'mode1welcome.wav'
welcome2 = 'mode2welcome.wav'
welcome3 = 'mode3welcome.wav'
welcome4 = 'mode4welcome.wav'
normal = 'normal.wav'
instructedcth = 'instructed0.wav'
coach = 'coached.wav' #for coaching in the first three modes
instructedSet3 = 'instructed2-3.wav'
instructedSet2 = 'instructed2-2.wav'
instructedSet1 = 'instructed2-1.wav'
instructedVmatch = 'instructed3.wav'
ghostCoach = 'coached4.wav'

try:
	fast = '/home/eternity/catkin_ws/src/can_to_ros/fastSound.wav' #path from typical installation
	playsound(fast)
except:
	print('you need to change the absolute path to the sound files in "can_coach_subs.py"')
slow = '/home/eternity/catkin_ws/src/can_to_ros/slowSound.wav' #path from typical installation 

def printit():
	"""This is the function that gives the sound feedback to the driver. It need to know the 'mode', or test that the driver is in.
	It subscribes to both the mode, and keeps track of the current mode."""
		
	t = threading.currentThread()#Timer(0.5, printit)
	global relv
	global feedbackType
	global setPoint
	rospy.set_param('relv', relv) #need to make this into a publisher
	while getattr(t,"do_run", True):
		print(mode, feedbackType,setPoint, th)
		if feedbackType == 0:
			pass
		elif feedbackType == 1: #this is used for tests 1 and 2
			print(th, lead, relv)
			if th > 2.25+thBounds: #+0.05
				rospy.loginfo("faster")
				playsound(fast)
			if th < 2.25-thBounds and th != -1: #-0.05
				playsound(slow)
				rospy.loginfo("slower")
		elif feedbackType == 2: #this is used for test 3
			print(relv)
			if relv > 0 + 0.4: #0.4 m/s is less than 1 mph
				rospy.loginfo("faster vmatch")
				playsound(fast)
			if relv < 0 - 0.4: #0.4 m/s is less than 1 mph
				rospy.loginfo("slower vmatch")
				playsound(slow)
		if mode == 8: #this is used for test 4
			print('you got to ghost mode')
			#make sure to add a print() that reflects the data being processed for this test
			#do something to start the bagfile?
			#subscribe to the ghost topic, ghostTh calculated from velocity and ghostSpacing
			if ghostTh > setPoint+thBounds:
				rospy.loginfo("faster")
				playsound(fast)
			if ghostTh < setPoint-thBounds and ghostTh != -1:
				playsound(slow)
				rospy.loginfo("slower")
		time.sleep(0.3)
	print("Stopping sound thread, as you wish.")

def callback869(data):
    global gnewLeadMeasurement
    gnewLeadMeasurement = data.point.x

def callbackvel(data):
    global gnewVel 
    gnewVel= data.twist.linear.x

def callback384(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])
    
def callback385(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])
    
def callback386(data):
	global gmyDetections
	gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])

def callback387(data):
	global gmyDetections
	gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])

def callback388(data):
	global gmyDetections
	gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])

def callback389(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])

def callback390(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])

def callback391(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])

def callback392(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])

def callback393(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])

def callback394(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])
    
def callback395(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])
 
def callback396(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])
  
def callback397(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])
    
def callback398(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])

def callback399(data):
    global gmyDetections
    gmyDetections.append([data.pose.position.x, data.pose.position.y,data.pose.position.z])

#subscribe to the mode message
	#0 is standby -- no can coach feedback
	#1 is cth
	#2 is dth
	#3 is vmatch
	#4 is ghost car
		#wherever bagfile starts, publish ghostTh
def callbackMode(data):
	global mode
	mode = data.data

#subscribe to th set point message -- thSet
	#1 is 1.35
	#2 is 1.8
	#3 is 2.25
def callbackSetPoint(data):
	global setPoint
	setPoint = data.data
def callbackFeedbackType(data): #none = 0, th = 1, vmatch = 2
	global feedbackType
	feedbackType = data.data

 
try:
	rospy.init_node('can_coach_subs', anonymous=True)
	rospy.Subscriber("/vehicle/vel", TwistStamped,callbackvel)
	print('subscribing')
	rospy.Subscriber("/vehicle/distanceEstimator/dist", PointStamped, callback869)
	#radar messages
	rospy.Subscriber("/track_a0", Marker, callback384)
	rospy.Subscriber("/track_a1", Marker, callback385)
	rospy.Subscriber("/track_a2", Marker, callback386)
	rospy.Subscriber("/track_a3", Marker, callback387)
	rospy.Subscriber("/track_a4", Marker, callback388)
	rospy.Subscriber("/track_a5", Marker, callback389)
	rospy.Subscriber("/track_a6", Marker, callback390)
	rospy.Subscriber("/track_a7", Marker, callback391)
	rospy.Subscriber("/track_a8", Marker, callback392)
	rospy.Subscriber("/track_a9", Marker, callback393)
	rospy.Subscriber("/track_a10", Marker, callback394)
	rospy.Subscriber("/track_a11", Marker, callback395)
	rospy.Subscriber("/track_a12", Marker, callback396)
	rospy.Subscriber("/track_a13", Marker, callback397)
	rospy.Subscriber("/track_a14", Marker, callback398)
	rospy.Subscriber("/track_a15", Marker, callback399)
	#director messages
	rospy.Subscriber("/setpoint", Float64, callbackSetPoint)
	rospy.Subscriber("/mode", UInt8, callbackMode)
	rospy.Subscriber("/feedback_type",UInt8, callbackFeedbackType)
	

	r = rospy.Rate(50)
	velocity = gnewVel
	lastMode = mode
	lastSetPoint = setPoint
	t = threading.Thread(target = printit)
	t.start()
	while not rospy.is_shutdown():
		print('starting while loop')
		
		while not rospy.is_shutdown():
			
			if velocity > 0:
				th = (leader.get_coords()[0])/(velocity) #distance divided by meters per second
			else:
				th = -1
			leader.predict()
			if gnewLeadMeasurement != None:#if there's a new 869 lead measurement
				#cluster 869 and radar points and choose one radar point
				if len(gmyDetections) > 0: # if there are new radar measurements
					labels = lt.clusterRadar([gnewLeadMeasurement,0],gmyDetections) #labels are points within 1m euclidean distance
					myPoints = labels 
					
					if len(myPoints) > 0: #if there is a point other than from 869 in cluster
						iLead = random.choice(myPoints)#just choose one randomly
						lead = gmyDetections[iLead][0:2] #lead coordinates
						relv = gmyDetections[iLead][2]
						gnewLeadMeasurement = None
						gmyDetections = [] #reset the radar message buffer
						leader.update(lead) #update kf
			else:
				if len(gmyDetections) > 64: # if there are 64 radar measurements and no gnewLeadMeasurement
					labels = lt.clusterRadar(leader.get_coords().tolist(),gmyDetections) #cluster algorithm gives labels
					myPoints = labels
					
					if len(myPoints) > 0: #if there is a point other than from kalman value in cluster
						iLead = random.choice(myPoints)#just choose one randomly
						lead = gmyDetections[iLead][0:2] #lead coordinates
						relv = gmyDetections[iLead][2] #lead relv
						
						gmyDetections = []#reset the radar message buffer
						leader.update(lead) #update kf
        #this feedback system operates under the assumption that there is a lead vehicle
			velocity = gnewVel
            #maybe have the sounds play in here?
			if mode != lastMode:
				if mode == 1: 
					print('entering mode 1')
					playsound(soundpath+welcome1)
					playsound(soundpath+normal)
					#print('Vmatch instructed') not implemented yet, currently normal
				if mode == 2:
					print('entering mode 2')
					playsound(soundpath+instructedcth)
					 #print('Vmatch coached')
				if mode == 3: 
					print('entering mode 3')
					playsound(soundpath+coach)
					#print('Normal Driving')
				if mode == 4: 
					playsound(soundpath+welcome2)
					#print('Drive with a 2.25 second th')
				if mode == 5: 
					playsound(soundpath+coach)
					#print('Listen to CAN coach, 2.25 s th.')
				if mode == 6: 
					playsound(soundpath+instructedVmatch)
					#print('Attempt to drive with the specified following distance. It will change minute by minute.')
				if mode == 7: 
					playsound(soundpath+coach)
					#print('Listen to can coach.')
				if mode == 8: 
					playsound(soundpath+ghostCoach)
					#print('Listen to CAN Coach, you are following a virtual car.')
				
				lastMode = mode
			if setPoint != lastSetPoint:
				if setPoint == 1.35:
					playsound(soundpath+instructedSet1)
					print('drive with set 1')
				if setPoint == 1.8:
					playsound(soundpath+instructedSet2)
					print('drive with set 2')
				if setPoint == 2.25:
					playsound(soundpath+instructedSet3)
					print('drive with set 3')
				
				lastSetPoint = setPoint
            
		print('before sleep')
		# t.cancel()
		t.do_run = False
		t.join()
		r.sleep()
	print('before spin')
	# t.cancel()
	t.do_run = False
	t.join()
except ValueError:
    print("Oops!  Try again...")
