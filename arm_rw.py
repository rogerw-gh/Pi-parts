#!/usr/bin/env python
from flask import Flask, render_template, Response

import os

#import servoblst as servo

app = Flask(__name__)

# First Set Up the Servos
# Going to use lists for this
SNums = [0,1,2,3] #Numbers of the Servos we'll be using in ServoBlaster
SName = ["Waist","Left","Right","Claw"] #Names of Servos
AInis = [90,152,90,60] #Initial angle for Servos 0-3
AMins = [0,60,40,60] #Minimum angles for Servos 0-3
AMaxs = [180,165,180,180] #Maximum angles for Servos 0-3
ACurs = AInis #Current angles being set as the intial angles
Step = 5
for i in range(4):
	print(SNums[i],AInis[i],AMins[i],AMaxs[i],ACurs[i])

os.system('sudo /home/pi/PiBits/ServoBlaster/user/servod --idle-timeout=2000') #This line is sent to command line to start the servo controller

def AAdd(Servo):
	if ACurs[Servo] < AMaxs[Servo]:
		ACurs[Servo] = ACurs[Servo]+Step
	#	micro = (1000 + (ACurs[Servo] * 5.555))
		micro = (1000 + (ACurs[Servo] * 8.3333))
		print(ACurs[Servo],micro)
		os.system("echo %d=%dus > /dev/servoblaster" % (SNums[Servo],micro))
	else:
		print "Max Angle Reached",SName[Servo],"Servo"

def ASub(Servo):
	if ACurs[Servo] > AMins[Servo]:
		ACurs[Servo] = ACurs[Servo]-Step
	#	micro = (1000 + (ACurs[Servo] * 5.555))
		micro = (1000 + (ACurs[Servo] * 8.3333))
		print(ACurs[Servo],micro)
		os.system("echo %d=%dus > /dev/servoblaster" % (SNums[Servo],micro))

	else:
		print "Min Angle Reached",SName[Servo],"Servo"




@app.route('/')
def index():
	try:
		return render_template('arm.html')
	except Exception as e:
		print e
		pass
		
				
@app.route("/<direction>")
def move(direction):
	# Choose the direction of the request
	if direction == 'gopen':
                ASub(3)
		#grip.setAngle(45, claw)
        
	elif direction == 'gclose':
                AAdd(3)
		#grip.setAngle(90, claw)

	elif direction == 'eup':
                AAdd(1)
		#elbow.incAngle(10, left)

	elif direction == 'edown':
		ASub(1)
		#elbow.incAngle(-19, left)

	elif direction == 'sback':
		ASub(2)
                #shoulder.incAngle(-10, right)

	elif direction == 'sfwd':
		AAdd(2)
                #shoulder.incAngle(10, right)

	elif direction == 'hleft':
                AAdd(0)
		#hip.incAngle(-10, waist)

	elif direction == 'hright':
		ASub(0)
                #hip.incAngle(10, waist)

	return direction
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

#sc.clean_up()
	
