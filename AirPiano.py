from pydub import AudioSegment
import time,os, csv
from pydub.playback import play
import sys,heapq
sys.path.insert(0, "LeapSDK/lib")
import Leap
from threading import Thread
from PianoListener import PianoListener
from uploaddata import UploadFile
class AirPiano(object):
	def __init__(self):
		self.output = [[],[],[],[],[]]
		self.listener = PianoListener()
		self.controller = Leap.Controller()
		self.flag =[0, 0, 0, 0, 0, 0, 0, 0]
		self.action = [0, 0, 0, 0, 0]
		self.queue = []

	def gesound(self):
		do = AudioSegment.from_mp3("audio/hhh/1do.mp3")
		re = AudioSegment.from_mp3("audio/hhh/2re.mp3")
		mi = AudioSegment.from_mp3("audio/hhh/3mi.mp3")
		fa = AudioSegment.from_mp3("audio/hhh/4fa.mp3")
		so = AudioSegment.from_mp3("audio/hhh/5so.mp3")
		la = AudioSegment.from_mp3("audio/hhh/6la.mp3")
		ti = AudioSegment.from_mp3("audio/hhh/7ti.mp3")
		doo = AudioSegment.from_wav("audio/hhh/8doo.wav")
		return [do, re, mi, fa, so, la, ti, doo]

	def plays(self,drum,trigger, keytype, itype, db = 0):
		if trigger:
			sound = drum + db
			play(sound)
			#-----record------
			pass

	def getoutput(self):
		i=0
		check = 0
		filename="piano"
		if os.path.exists(filename + ".csv"):
			i=1
			check=1
		while os.path.exists(filename + str(i) + ".csv"):
			i+=1
		if check==0:
			nfilename=filename
		else:
			nfilename=filename+str(i)
		if self.output:
			output = list(heapq.merge(self.output[0],self.output[1],self.output[2],self.output[3],self.output[4]))
			f = open(nfilename + '.csv','wb')
			wr = csv.writer(f,quoting=csv.QUOTE_ALL)
			for row in output:
				wr.writerow(row)
			print "Piano Creation Saved."
			#------ upload patch-----
			f.close()
			os.system('clear')
			print "Uploading "+nfilename+ " to S3..."
			u = UploadFile()
			u.upload(nfilename + ".csv")
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
			try:
				for i, va in enumerate(self.listener.gest):
					self.getAction(i, va)
				if sum(self.action) != 0:
					self.queue.append(self.action)
					print self.action
					print "Add Action"
			except:
				print "Failed to get gest"

	def main(self):
		ct = 0.5
		#self.output = None
		keys = self.gesound()
		t_piano = [None for i in range(5)]
		while True:
			if self.queue:
				tempact = self.queue.pop(0)
				for j in range(5):
					if tempact[j] == 1:
						self.output[j].append((time.time(), j, "p"))
						t_piano[j]=Thread(target = self.plays, args=(keys[j],tempact[j], j,"p",25))
						t_piano[j].start()

if __name__ == "__main__":
	d = AirPiano()
	try:
		t_Drum = Thread(target=d.main)
		#t_Piano = Thread(target=p.main)
		t_Drum_Action = Thread(target=d.getaction)
		t_Drum.daemon = True
		#t_Piano.daemon = True
		t_Drum_Action.daemon = True
		t_Drum.start()
		t_Drum_Action.start()
		#t_Piano.start()
		while t_Drum.isAlive() and t_Drum_Action.isAlive():
			t_Drum.join(1)
			t_Drum_Action.join(1)
	except KeyboardInterrupt:
		#d.getoutput()
		d.controller.remove_listener(d.listener)
		exit
