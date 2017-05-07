from pydub import AudioSegment
import time
from pydub.playback import play
import boto3
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
		self.flag =[0,0,0,0]
		self.action = [0, 0, 0, 0]
		self.queue = []
		sqs = boto3.resource('sqs')
        self.q = sqs.get_queue_by_name(QueueName='#######')

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
					action_json = json.dumps(self.action)
					self.q.send_message(MessageBody=action_json)
					print "Add Action"
					print "t",time.time() - start
					# time.sleep(0.1)
			except:
				print "Failed to get gest"

	# def getSync(self):
	# 	self.controller.add_listener(self.listener)
	# 	time.sleep(1)
	# 	while True:
	# 		#starts = self.get_pygame_events()
	# 		#a,s,k,l = self.keyreturn(starts)
	# 		# print str(self.listener.gest)
	# 		try:
	# 			for i, va in enumerate(self.listener.gest):
	# 				self.getAction(i, va)
	# 			if sum(self.action) != 0:
	# 				self.queue.append(self.action)
	# 				print "Add Action"
	# 				print self.action
	# 				# time.sleep(0.1)
	# 		except:
	# 			print "Failed to get gest"

	def main(self):
		ct = 0.5
		self.output = None
		# tmain=Thread(target = stream.main)
		# tmain.start()

		drum1,drum2,drum3, drum4 = self.gesound()
		# pygame.init()

		#t5 = Thread(target = self.plays, args=(drum4, 400,self.action[3], +5,))
		while True:
			#start = time.time()
			if self.queue:
				print len(self.queue)
				tempact = self.queue.pop(0)
			#print a,s,k,l
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
		t1 = Thread(target=d.main)
		t2 = Thread(target=d.getaction)
		t1.daemon = True
		t2.daemon = True
		t1.start()
		t2.start()
		while t1.isAlive() and t2.isAlive():
			t1.join(1)
			t2.join(1)
	except KeyboardInterrupt:
		#d.getoutput()
		d.controller.remove_listener(d.listener)
		exit
