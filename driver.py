from pydub import AudioSegment
import time
from pydub.playback import play
# import boto3
import sys
sys.path.insert(0, "LeapSDK/lib")
import Leap
import time
from threading import Thread
from AirDrum import AirDrum
from AirPiano import AirPiano
class driver(object):
	def __init__(self):
		pass
	def main_driver(self):
		pass
if __name__ == "__main__":
	d = AirPiano()
	#p = AirPiano()
	try:
		t_Drum = Thread(target=d.main)
		t_Drum_Action = Thread(target=d.getaction)
		t_Drum.daemon = True
		t_Drum_Action.daemon = True
		t_Drum.start()
		t_Drum_Action.start()
		while t_Drum.isAlive() and t_Drum_Action.isAlive():
			t_Drum.join(1)
			t_Drum_Action.join(1)
	except KeyboardInterrupt:
		#d.getoutput()
		d.controller.remove_listener(d.listener)
		exit
