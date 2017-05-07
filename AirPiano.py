from pydub import AudioSegment
import time
from pydub.playback import play
import sys
sys.path.insert(0, "LeapSDK/lib")
import Leap
import time
from threading import Thread
from PianoListener import PianoListener

class AirPiano(object):
	def __init__(self):
		self.output = None
		self.listener = PianoListener()
		self.controller = Leap.Controller()
		self.flag =[0,0,0,0]
		self.action = [0, 0, 0, 0, 0, 0, 0, 0]
		self.queue = []

	def gesound(self):
		do = AudioSegment.from_mp3("audio/piano/1do.mp3")
		re = AudioSegment.from_mp3("audio/piano/2re.mp3")
		mi = AudioSegment.from_mp3("audio/piano/3mi.mp3")
		fa = AudioSegment.from_mp3("audio/piano/4fa.mp3")
		so = AudioSegment.from_mp3("audio/piano/5so.mp3")
		la = AudioSegment.from_mp3("audio/piano/6la.mp3")
		ti = AudioSegment.from_mp3("audio/piano/7ti.mp3")
		doo = AudioSegment.from_wav("audio/piano/8doo.wav")
		return [do, re, mi, fa, so, la, ti, doo]

	def plays(self,drum, lens,trigger, db = 0):
		if trigger:
			# if lens != -1:
			# 	sound = drum[:lens] + db
			# else:
			sound = drum + db
			play(sound)
			#-----record------
			if not self.output:
				self.output = sound
			else:
				self.output += sound
			pass

	def getoutput(self):
		file_handle = self.output.export("/data/piano.wav", format="wav")
		pass

	def getAction(self, i, va):
		if va == 1 and self.flag[i] == 1: #state 1 -> 1
				self.action[i] = 0
		elif va == 1 and self.flag[i] == 0: #state 0 -> 1
			self.action[i] = 1
			self.flag[i] = 1
		elif va == 0 and self.flag[i] == 0: #state 0 -> 0
			self.action[i] = 0
		elif va == 0 and self.flag[i] == 1: #state 1 -> 0
			self.action[i] = 0
			self.flag[i] = 0
		pass

	def getaction(self):
		self.controller.add_listener(self.listener)
		time.sleep(1)
		while True:
			start = time.time()
			#starts = self.get_pygame_events()
			#a,s,k,l = self.keyreturn(starts)
			# print str(self.listener.gest)
			try:
				for i, va in enumerate(self.listener.gest):
					self.getAction(i, va)
				if sum(self.action) != 0:
					self.queue.append(self.action)
					print "Add Action"
					print "t",time.time() - start
					# time.sleep(0.1)
			except:
				print "Failed to get gest"

	def main(self):
		ct = 0.5
		self.output = None
		drum1,drum2,drum3, drum4 = self.gesound()
		while True:
			#start = time.time()
			if self.queue:
				print len(self.queue)
				tempact = self.queue.pop(0)

				if tempact[0] == 1:
					t1=Thread(target = self.plays, args=(drum1,600,tempact[0],+5,))
					t1.start()
				if tempact[1] == 1:
					t2 = Thread(target = self.plays, args=(drum2,400,tempact[1],+15))
					t2.start()
				if tempact[2] == 1:
					t3=Thread(target = self.plays, args=(drum3, 500,tempact[2], +25,))
					t3.start()
				if tempact[3] == 1:
					t4 = Thread(target = self.plays, args=(drum4, 400,tempact[3], +15,))
					t4.start()
				# t1.setDaemon(True)
				# t2.setDaemon(True)
				# t3.setDaemon(True)
				# t4.setDaemon(True)




			#print time.time() - start
			# self.listener.setgest()
			# time.sleep(0.1)
			#self.listener.setgest()

if __name__ == "__main__":
	d = AirDrum()
	try:
		t_Drum = Thread(target=d.main)
		t_Piano = Thread(target=d.main)
		t2 = Thread(target=d.getaction)
		t_Drum.daemon = True
		t2.daemon = True
		t_Drum.start()
		t_Drum.start()
		while t_Drum.isAlive() and t2.isAlive():
			t_Drum.join(1)
			t2.join(1)
	except KeyboardInterrupt:
		#d.getoutput()
		d.controller.remove_listener(d.listener)
		exit
