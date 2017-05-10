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
	try:
		while True:
			#drum mode
			curr_mode = 0
			d = AirDrum()
			t_Drum = Thread(target=d.main)
			t_Drum_Action = Thread(target=d.getaction)
			t_Drum.daemon = True
			t_Drum_Action.daemon = True
			t_Drum.start()
			t_Drum_Action.start()
			#print type(d.listener)
			time.sleep(0.5)
			while d.listener.switch == False and t_Drum.isAlive() and t_Drum_Action.isAlive():
				#print "Drum Mode"
				t_Drum.join(1)
				t_Drum_Action.join(1)
			d.getoutput()
			d.controller.remove_listener(d.listener)

			# piano mode
			curr_mode = 1
			p = AirPiano()
			t_Piano = Thread(target=p.main)
			t_Piano_Action = Thread(target=p.getaction)
			t_Piano.daemon = True
			t_Piano_Action.daemon = True
			t_Piano.start()
			t_Piano_Action.start()
			time.sleep(0.5)
			#print "Piano Mode"
			while p.listener.switch == False and t_Piano.isAlive() and t_Piano_Action.isAlive():
				t_Piano.join(1)
				t_Piano_Action.join(1)
			p.getoutput()
			p.controller.remove_listener(p.listener)
	except KeyboardInterrupt:
		print "ending"
		if curr_mode == 0:
			#print "delete drumaklshjdjkashdjaksdhjaksdhjkahdjksahdkjashdjksahdkjasdhkjasdh"
			#print d.output,"aha"
			d.getoutput()
			d.controller.remove_listener(d.listener)
		else:
			#print p.output,"aha"
			p.getoutput()
			p.controller.remove_listener(p.listener)
		exit
