from pydub import AudioSegment
import time,os,csv,heapq
from pydub.playback import play
import sys
sys.path.insert(0, "LeapSDK/lib")
import Leap
from threading import Thread
from DrumListener import DrumListener
from uploaddata import UploadFile
class AirDrum(object):
	def __init__(self):
		self.output = [[],[],[],[]]
		self.listener = DrumListener()
		self.controller = Leap.Controller()
		self.flag =[0,0,0,0]
		self.action = [0, 0, 0, 0]
		self.queue = []

	def gesound(self):
		drum1 = AudioSegment.from_wav("audio/snare.wav")
		drum2 = AudioSegment.from_wav("audio/cymbals.wav")
		drum3 = AudioSegment.from_wav("audio/kick.wav")
		drum4 = AudioSegment.from_wav("audio/hat.wav")
		return drum1,drum2,drum3, drum4

	def plays(self,drum, lens,trigger, keytype, itype,db = 0):
		if trigger:
			if lens != -1:
				sound = drum[:lens] + db
			else:
				sound = drum + db
			play(sound)
			#-----record------
			self.output[keytype].append((time.time(), keytype, itype))
			pass

	def getoutput(self):
		i=0
		check = 0
		filename="drum"
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
			print "#########################################################################"
			output = list(heapq.merge(self.output[0],self.output[1],self.output[2],self.output[3]))
			f = open(nfilename + '.csv','wb')
			wr = csv.writer(f,quoting=csv.QUOTE_ALL)
			for row in output:
				wr.writerow(row)
			print "Drum Creation Saved."
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
			#starts = self.get_pygame_events()
			#a,s,k,l = self.keyreturn(starts)
			# print str(self.listener.gest)
			try:
				for i, va in enumerate(self.listener.gest):
					self.getAction(i, va)
				if sum(self.action) != 0:
					#print self.action
					self.queue.append(self.action)
					print "Add Action"
					# print "t",time.time() - start
					# time.sleep(0.1)
			except:
				print "Failed to get gest"

	def main(self):
		ct = 0.5
		drum1,drum2,drum3, drum4 = self.gesound()
		while True:
			#start = time.time()
			if self.queue:
				#print self.queue
				tempact = self.queue.pop(0)
				#print tempact
				if tempact[0] == 1:
					t1=Thread(target = self.plays, args=(drum1,600,tempact[0],0,"d",+5))
					t1.start()
				if tempact[1] == 1:
					t2 = Thread(target = self.plays, args=(drum2,400,tempact[1],1,"d",+15))
					t2.start()
				if tempact[2] == 1:
					t3=Thread(target = self.plays, args=(drum3, 500,tempact[2],2,"d", +25))
					t3.start()
				if tempact[3] == 1:
					t4 = Thread(target = self.plays, args=(drum4, 400,tempact[3],3,"d", +15))
					t4.start()

if __name__ == "__main__":
	d = AirDrum()
	#p = AirPiano()
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
