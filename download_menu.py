import boto3
import json,os,time
from pydub import AudioSegment
from pydub.playback import play
import sys,csv
from mixer import Mixer

class DownloadFile(object):
    def __init__(self):
        pass
    def initialize(self):
        json_file = "../keys.json"
        AWS_ACCESS_KEY, AWS_SECRET_KEY = self.load_keys(json_file)
        self.s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    def load_keys(self, json_file):
        with open(json_file) as data_file:
            data = json.load(data_file)
            access_key = data["access_key"]
            secret_Key = data["secret_Key"]
            return access_key, secret_Key

    def menu(self):
        self.initialize()
        os.system('clear')
        bucketname = 'AirDrum'
        ind = 1
        pulls = self.s3.list_objects(Bucket=bucketname)['Contents']
        filenames = ["" for i in range(len(pulls))]
        for element in pulls:
            print ind,element['Key']
            filenames[ind - 1] = element['Key']
            ind += 1
        picked = raw_input("pick the file number you want to select:")
        fname = filenames[int(picked) - 1]
        self.s3.download_file('AirDrum', fname, fname)
        print "Downloaded."
        self.playit(fname)
        time.sleep(1)
    def playit(self,file):
        "Playing..."
        self.mixer(file)
        os.system('clear')
        print "Done."
        pass
    def getd(self):
        drum1 = AudioSegment.from_wav("audio/snare.wav")
        drum2 = AudioSegment.from_wav("audio/cymbals.wav")
        drum3 = AudioSegment.from_wav("audio/kick.wav")
        drum4 = AudioSegment.from_wav("audio/hat.wav")
        return [drum1,drum2,drum3, drum4]

    def getp(self):
        do = AudioSegment.from_mp3("audio/hhh/1do.mp3")
        re = AudioSegment.from_mp3("audio/hhh/2re.mp3")
        mi = AudioSegment.from_mp3("audio/hhh/3mi.mp3")
        fa = AudioSegment.from_mp3("audio/hhh/4fa.mp3")
        so = AudioSegment.from_mp3("audio/hhh/5so.mp3")
        la = AudioSegment.from_mp3("audio/hhh/6la.mp3")
        ti = AudioSegment.from_mp3("audio/hhh/7ti.mp3")
        doo = AudioSegment.from_wav("audio/hhh/8doo.wav")
        return [do, re, mi, fa, so, la, ti, doo]
    def mixer(self, keys, drums, file):
        drums = self.getd()
        keys = self.getp()
        #------process file-----

        pass
sys.path.insert(0, "LeapSDK/lib")


if __name__ == '__main__':
    m = DownloadFile()
    try:
        while True:
            m.menu()
    except KeyboardInterrupt:
        exit
