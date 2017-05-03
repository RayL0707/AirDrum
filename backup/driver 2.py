from pydub import AudioSegment
import time,pygame
from pydub.playback import play
import sys
sys.path.insert(0, "LeapSDK/lib")
import Leap
import time
from threading import Thread
from app import SampleListener

class AirDrum(object):
	def __init__(self):
		self.output = None
		self.listener = SampleListener()
		self.controller = Leap.Controller()
		pass
	def gesound(self):
		drum1 = AudioSegment.from_wav("audio/snare.wav")
		drum2 = AudioSegment.from_wav("audio/cymbals.wav")
		drum3 = AudioSegment.from_wav("audio/kick.wav")
		drum4 = AudioSegment.from_wav("audio/hat.wav")
		return drum1,drum2,drum3, drum4
	def plays(self,drum, lens,trigger, db = 0):
		if trigger:
			if lens != -1:
				sound = drum[:lens] + db
			else:
				sound = drum + db
			play(sound)
			#-----record------
			if not self.output:
				self.output = sound
			else:
				self.output += sound
			pass

	def get_pygame_events(self):
		pygame.init()
		pygame_events = pygame.event.get()
		return pygame_events
		pass

	def getoutput(self):
		file_handle = self.output.export("/data/output.wav", format="wav")
		pass


	def keyreturn(self,events):
		a = s = k = l = False
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					a = True
				if event.key == pygame.K_s:
					s = True
				if event.key == pygame.K_k:
					k = True
				if event.key == pygame.K_l:
					l = True
		return a,s,k,l
	def main(self):
		ct = 0.5
		self.output = None
		self.controller.add_listener(self.listener)

		# tmain=Thread(target = stream.main)
		# tmain.start()
		drum1,drum2, drum3, drum4 = self.gesound()
		pygame.init()
		while True:
			starts = self.get_pygame_events()
			#a,s,k,l = self.keyreturn(starts)
			a,s,k,l = self.listener.gest
			#print a,s,k,l
			t1=Thread(target = self.plays, args=(drum1,600,a,+5,))
			t2 = Thread(target = self.plays, args=(drum2,400,s,+25))
			t3=Thread(target = self.plays, args=(drum3, 500,k, +35,))
			t4 = Thread(target = self.plays, args=(drum4, 400,l, +5,))
			t1.setDaemon(True)
			t2.setDaemon(True)
			t3.setDaemon(True)
			t4.setDaemon(True)
			t1.start()
			t2.start()
			t3.start()
			t4.start()
			# self.listener.setgest()
			# time.sleep(0.1)
			#self.listener.setgest()
		pass

if __name__ == "__main__":
	try:
		d = AirDrum()
		d.main()
	except KeyboardInterrupt:
		#d.getoutput()
		d.controller.remove_listener(d.listener)
		exit
