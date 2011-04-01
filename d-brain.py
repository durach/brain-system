# -*- coding: utf8 -*-

import sys
import os

os.chdir(os.path.dirname(__file__))
sys.path.append('libs')
#sys.stderr = open('stderr.txt','w')
#sys.stdout = sys.stderr

import dBrain
import agentJoystick
import agentKEUSB24R

if __name__ == '__main__':
	e = dBrain.dBrain(
		(425, 190),
		'D-Brain'
	)
	e.run([
		agentJoystick.agent(),
		agentKEUSB24R.agent()
	])
