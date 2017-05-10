import boto3
import json,os,time
from pydub import AudioSegment
from pydub.playback import play
import sys

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

    def manu(self):
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
        sound = AudioSegment.from_wav(file)
        play(sound)
        os.system('clear')
        print "Done."

sys.path.insert(0, "LeapSDK/lib")


if __name__ == '__main__':
    m = DownloadFile()
    try:
        while True:
            m.manu()
    except KeyboardInterrupt:
        exit
