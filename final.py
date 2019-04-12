from multiprocessing import Process, Queue
import time
import cv2
import RPi.GPIO as GIPO
import numpy as np

# Upper limit
_Servo1UL = 175
_Servo0UL = 250

# Lower Limit
_Servo1LL = 120
_Servo0LL = 50

# Resolution Size
_X = 480
_Y = 360
_X_Quarter = _X / 4
_Y_Quarter = _Y / 4

# clock unit for PWM
_Horizontal_Default = 7.5
_Vertical_Default = 5
_One_Tick = .1

# Setting GPIO in pi
GPIO.setmode(GPIO.BCM)

#p1.ChangeDutyCycle(
try:
    while True:
        #7.5 90%     2.5 0%    12.5 180%
        p1.ChangeDutyCycle(7.5)
        print("somethings happening 1")
        time.sleep(1)
        p1.ChangeDutyCycle(12.5)
        print("somethings happening 1")
        time.sleep(1)
        p1.ChangeDutyCycle(2.5)
        print("somethings happening 1")
        time.sleep(3)
except KeyboardInterrupt:




#ServoBlaster = open('/dev/servoblaster', 'w')		# ServoBlaster is what we use to control the servo motors

webcam = cv2.VideoCapture(-1)				# Get ready to start getting images from the webcam
webcam.set(3, _X)		# I have found this to be about the highest-
webcam.set(4, _Y)	# 	resolution you'll want to attempt on the pi

frontalCascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')		# frontal face pattern detection
profileface = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_profileface.xml')		# side face pattern detection

face = [0,0,0,0]	# This will hold the array that OpenCV returns when it finds a face: (makes a rectangle)
Cface = [0,0]		# Center of the face: a point calculated from the above variable
lastface = 0		# int 1-3 used to speed up detection. The script is looking for a right profile face,-
			# 	a left profile face, or a frontal face; rather than searching for all three every time,-
			# 	it uses this variable to remember which is last saw: and looks for that again. If it-
			# 	doesn't find it, it's set back to zero and on the next loop it will search for all three.-
			# 	This basically tripples the detect time so long as the face hasn't moved much.
"""
Servo0CP = Queue()	# Servo zero current position, sent by subprocess and read by main process
Servo1CP = Queue()	# Servo one current position, sent by subprocess and read by main process
Servo0DP = Queue()	# Servo zero desired position, sent by main and read by subprocess
Servo1DP = Queue()	# Servo one desired position, sent by main and read by subprocess
Servo0S = Queue()	# Servo zero speed, sent by main and read by subprocess
Servo1S = Queue()	# Servo one speed, sent by main and read by subprocess
"""

def HorizontalServo():
	pin0 = 18
	GPIO.setup(pin0, GPIO.OUT)
	p0 = GPIO.PWM(pin0, 50)
	p0.start(2.5)
	
def VerticalServo():
	pin1 = 17
	GPIO.setup(pin1, GPIO.OUT)
	p1 = GPIO.WPM(pin1, 50)
	p1.start(2.5)

"""
def P0():	# Process 0 controlles servo0
	speed = .1		# Here we set some defaults:
	_Servo0CP = 99		# by making the current position and desired position unequal,-
	_Servo0DP = 100		# 	we can be sure we know where the servo really is. (or will be soon)
	while True:
		time.sleep(speed)
		if Servo0CP.empty():			# Constantly update Servo0CP in case the main process needs-
			Servo0CP.put(_Servo0CP)		# 	to read it
		if not Servo0DP.empty():		# Constantly read read Servo0DP in case the main process-
			_Servo0DP = Servo0DP.get()	#	has updated it
		if not Servo0S.empty():			# Constantly read read Servo0S in case the main process-
			_Servo0S = Servo0S.get()	# 	has updated it, the higher the speed value, the shorter-
			speed = .1 / _Servo0S		# 	the wait between loops will be, so the servo moves faster
		if _Servo0CP < _Servo0DP:					# if Servo0CP less than Servo0DP
			_Servo0CP += 1						# incriment Servo0CP up by one
			Servo0CP.put(_Servo0CP)					# move the servo that little bit
			ServoBlaster.write('0=' + str(_Servo0CP) + '\n')	#
			ServoBlaster.flush()					#
			if not Servo0CP.empty():				# throw away the old Servo0CP value,-
				trash = Servo0CP.get()				# 	it's no longer relevent
		if _Servo0CP > _Servo0DP:					# if Servo0CP greater than Servo0DP
			_Servo0CP -= 1						# incriment Servo0CP down by one
			Servo0CP.put(_Servo0CP)					# move the servo that little bit
			ServoBlaster.write('0=' + str(_Servo0CP) + '\n')	#
			ServoBlaster.flush()					#
			if not Servo0CP.empty():				# throw away the old Servo0CP value,-
				trash = Servo0CP.get()				# 	it's no longer relevent
		if _Servo0CP == _Servo0DP:	        # if all is good,-
			_Servo0S = 1		        # slow the speed; no need to eat CPU just waiting
			

def P1():	# Process 1 controlles servo 1 using same logic as above
	speed = .1
	_Servo1CP = 99
	_Servo1DP = 100
	while True:
		time.sleep(speed)
		if Servo1CP.empty():
			Servo1CP.put(_Servo1CP)
		if not Servo1DP.empty():
			_Servo1DP = Servo1DP.get()
		if not Servo1S.empty():
			_Servo1S = Servo1S.get()
			speed = .1 / _Servo1S
		if _Servo1CP < _Servo1DP:
			_Servo1CP += 1
			Servo1CP.put(_Servo1CP)
			ServoBlaster.write('1=' + str(_Servo1CP) + '\n')
			ServoBlaster.flush()
			if not Servo1CP.empty():
				trash = Servo1CP.get()
		if _Servo1CP > _Servo1DP:
			_Servo1CP -= 1
			Servo1CP.put(_Servo1CP)
			ServoBlaster.write('1=' + str(_Servo1CP) + '\n')
			ServoBlaster.flush()
			if not Servo1CP.empty():
				trash = Servo1CP.get()
		if _Servo1CP == _Servo1DP:
			_Servo1S = 1
"""


Process(target=P0, args=()).start()	# Start the subprocesses
Process(target=P1, args=()).start()	#
time.sleep(1)				# Wait for them to start

#====================================================================================================

"""
def CamRight( distance, speed ):		# To move right, we are provided a distance to move and a speed to move.
	global _Servo0CP			# We Global it so  everyone is on the same page about where the servo is...
	if not Servo0CP.empty():		# Read it's current position given by the subprocess(if it's avalible)-
		_Servo0CP = Servo0CP.get()	# 	and set the main process global variable.
	_Servo0DP = _Servo0CP + distance	# The desired position is the current position + the distance to move.
	if _Servo0DP > _Servo0UL:		# But if you are told to move further than the servo is built go...
		_Servo0DP = _Servo0UL		# Only move AS far as the servo is built to go.
	Servo0DP.put(_Servo0DP)			# Send the new desired position to the subprocess
	Servo0S.put(speed)			# Send the new speed to the subprocess
	return;

def CamLeft(distance, speed):			# Same logic as above
	global _Servo0CP
	if not Servo0CP.empty():
		_Servo0CP = Servo0CP.get()
	_Servo0DP = _Servo0CP - distance
	if _Servo0DP < _Servo0LL:
		_Servo0DP = _Servo0LL
	Servo0DP.put(_Servo0DP)
	Servo0S.put(speed)
	return;


def CamDown(distance, speed):			# Same logic as above
	global _Servo1CP
	if not Servo1CP.empty():
		_Servo1CP = Servo1CP.get()
	_Servo1DP = _Servo1CP + distance
	if _Servo1DP > _Servo1UL:
		_Servo1DP = _Servo1UL
	Servo1DP.put(_Servo1DP)
	Servo1S.put(speed)
	return;


def CamUp(distance, speed):			# Same logic as above
	global _Servo1CP
	if not Servo1CP.empty():
		_Servo1CP = Servo1CP.get()
	_Servo1DP = _Servo1CP - distance
	if _Servo1DP < _Servo1LL:
		_Servo1DP = _Servo1LL
	Servo1DP.put(_Servo1DP)
	Servo1S.put(speed)
	return;
"""
def CamRight(num):
	#for i in range(num):
		p0.ChangeDutyCycle(_One_Tick)
def CamLeft(num):
	#for i in range(num):
		p0.ChangeDutyCycle(- _One_Tick)
def CamDown(num):
	#for i in range(num):
		p1.ChangeDutyCycle(_One_Tick)
def CamUp(num):
	#for i in range(num):
		p1.ChangeDutyCycle(- _One_Tick)
#============================================================================================================


while True:

	faceFound = False	# This variable is set to true if, on THIS loop a face has already been found
				# We search for a face three diffrent ways, and if we have found one already-
				# there is no reason to keep looking.
	
	if not faceFound:
		if lastface == 0 or lastface == 1:
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			fface = frontalface.detectMultiScale(aframe,1.3, 3,(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(60,60))
			if fface != ():			# if we found a frontal face...
				lastface = 1		# set lastface 1 (so next loop we will only look for a frontface)
				for f in fface:		# f in fface is an array with a rectangle representing a face
					faceFound = True
					face = f

	if not faceFound:				# if we didnt find a face yet...
		if lastface == 0 or lastface == 2:	# only attempt it if we didn't find a face last loop or if-
			aframe = webcam.read()[1]	# 	THIS method was the one who found it last loop	# since the frontalface search above
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			pfacer = profileface.detectMultiScale(aframe,1.3, 3,(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(80,80))
			if pfacer != ():		# if we found a profile face...
				lastface = 2
				for f in pfacer:
					faceFound = True
					face = f

	if not faceFound:				# a final attempt
		if lastface == 0 or lastface == 3:	# this is another profile face search, because OpenCV can only-
			aframe = webcam.read()[1]	#	detect right profile faces, if the cam is looking at-
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			cv2.flip(aframe,1,aframe)	#	flip the image
			pfacel = profileface.detectMultiScale(aframe,1.3, 3,(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(80,80))
			if pfacel != ():
				lastface = 3
				for f in pfacel:
					faceFound = True
					face = f

	if not faceFound:		# if no face was found...-
		lastface = 0		# 	the next loop needs to know
		face = [0,0,0,0]	# so that it doesn't think the face is still where it was last loop

		# 240 180 40 40
	x,y,w,h = face
	Cface = [(w/2+x),(h/2+y)]	# we are given an x,y corner point and a width and height, we need the center
	print (str(Cface[0]) + "," + str(Cface[1]))

	
	if x != 0:
		if x < _X_Quarter:
			CamLeft(_One_Tick)
		if x > _X - _X_Quarter:
			CamRight(- _One_Tick)
		if y < _Y_Quarter:
			CamUp(_One_Tick)
		if y > _Y - _Y_Quarter:
			CamDown(- _One_Tick)
			
	
	"""
	if Cface[0] != 0:		# if the Center of the face is not zero (meaning no face was found)

		if Cface[0] > 180:	# The camera is moved diffrent distances and speeds depending on how far away-
			CamLeft(5,1)	#	from the center of that axis it detects a face
		if Cface[0] > 190:	#
			CamLeft(7,2)	#
		if Cface[0] > 200:	#
			CamLeft(9,3)	#

		if Cface[0] < 140:	# and diffrent dirrections depending on what side of center if finds a face.
			CamRight(5,1)
		if Cface[0] < 130:
			CamRight(7,2)
		if Cface[0] < 120:
			CamRight(9,3)

		if Cface[1] > 140:	# and moves diffrent servos depending on what axis we are talking about.
			CamDown(5,1)
		if Cface[1] > 150:
			CamDown(7,2)
		if Cface[1] > 160:
			CamDown(9,3)

		if Cface[1] < 100:
			CamUp(5,1)
		if Cface[1] < 90:
			CamUp(7,2)
		if Cface[1] < 80:
			CamUp(9,3)
	"""
    p1.stop()
    p2.stop()
    
GPIO.cleanup()
webcam.realease()
cv2.destroyAllWindows()

#echo 0=60 > /dev/servoblaster