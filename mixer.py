
import time,os,heapq,csv
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread
# A =[[],[]]
# A[0] =[(1111,1,"p"),(1112,2,"p")]
# A[1] = [(1110,0,"p"),(1113,0,"p")]
# res = list(heapq.merge(A[0],A[1]))
# f = open('record1.csv','wb')
# wr = csv.writer(f,quoting=csv.QUOTE_ALL)
# for el in res:
# 	wr.writerow(el)
class Mixer(object):
	def __init__(self,file):
		self.file = file
		self.keys = []
		self.drums = []
		pass
	def getd(self):
	  drum1 = AudioSegment.from_wav("audio/snare.wav")
	  drum2 = AudioSegment.from_wav("audio/cymbals.wav")
	  drum3 = AudioSegment.from_wav("audio/kick.wav")
	  drum4 = AudioSegment.from_wav("audio/hat.wav")
	  self.drums = [drum1,drum2,drum3, drum4]
	  pass

	def getp(self):
	  do = AudioSegment.from_mp3("audio/hhh/1do.mp3")
	  re = AudioSegment.from_mp3("audio/hhh/2re.mp3")
	  mi = AudioSegment.from_mp3("audio/hhh/3mi.mp3")
	  fa = AudioSegment.from_mp3("audio/hhh/4fa.mp3")
	  so = AudioSegment.from_mp3("audio/hhh/5so.mp3")
	  la = AudioSegment.from_mp3("audio/hhh/6la.mp3")
	  ti = AudioSegment.from_mp3("audio/hhh/7ti.mp3")
	  doo = AudioSegment.from_wav("audio/hhh/8doo.wav")
	  self.keys = [do, re, mi, fa, so, la, ti, doo]
	  pass
	def plays(self,drum, keytype,itype,lens,db = 0):
		if lens != -1:
			sound = drum[:lens] + db
		else:
			sound = drum + db
		play(sound)
		pass

	def mixer(self):
		self.getd()
		self.getp()
		t_pianos = [0 for i in range(5)]
		t_drums = [0 for i in range(4)]
		with open(self.file, 'rb') as f:
			reader = csv.reader(f)
			record = list(reader)
		#nd = 0
		start = time.time() - float(record[0][0])
		while True:
			if record:
				tempact = record.pop(0)
				while time.time() - start < float(tempact[0]):
					continue
				j = int(tempact[1])
				if tempact[2] == "p":
					t_pianos[j]=Thread(target = self.plays, args=(self.keys[j],j,"p",-1,25))
					t_pianos[j].start()
				elif tempact[2] == "d":
					#print "hi"
					# t_drums[j]=Thread(target = self.plays, args=(self.drums[j],j,"d",-1,25))
					# t_drums[j].start()
					if j == 0:
						t_drums[j]=Thread(target = self.plays, args=(self.drums[j],j,"d",600,5))
						t_drums[j].start()
					elif j == 1:
						t_drums[j] = Thread(target = self.plays, args=(self.drums[j],j,"d",400,15))
						t_drums[j].start()
					elif j == 2:
						t_drums[j]=Thread(target = self.plays, args=(self.drums[j],j,"d",500,25))
						t_drums[j].start()
					elif j == 3:
						t_drums[j] = Thread(target = self.plays, args=(self.drums[j],j,"d",400,15))
						t_drums[j].start()
				#ind += 1
			else:
				break
			#play(self.drums[int(record[ind][1])]) if record[ind][2] == "d" else play(self.keys[int(record[ind][1])])


if __name__ == '__main__':
	print time.time()
	test = Mixer('piano1.csv')
	test.mixer()
