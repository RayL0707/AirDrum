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
        time.sleep(1)
        os.system('clear')
        bucketname = 'AirDrum'
        ind = 1
        try:
            pulls = self.s3.list_objects(Bucket=bucketname)['Contents']
        except:
            qt = raw_input("There is no file on cloud.")
            time.sleep(1)
            raise KeyboardInterrupt
        filenames = ["" for i in range(len(pulls))]
        for element in pulls:
            print ind,element['Key']
            filenames[ind - 1] = element['Key']
            ind += 1
        picked = raw_input("pick the file number you want to select:")
        try:
            fname = filenames[int(picked) - 1]
        except:
            print "no such file."
            time.sleep(1)
            return
        self.s3.download_file('AirDrum', fname, fname)
        print "Downloaded."
        self.playit(fname)
        time.sleep(1)
    def playit(self,file):
        os.system('clear')
        "Playing..."
        playing = Mixer(file)
        playing.mixer()
        os.system('clear')
        print "Done."
        pass

        pass
sys.path.insert(0, "LeapSDK/lib")


if __name__ == '__main__':
    m = DownloadFile()
    try:
        while True:
            m.menu()
    except KeyboardInterrupt:
        exit
