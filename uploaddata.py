import boto3
import json

class UploadFile(object):
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

    def upload(self, filename):
        self.initialize()
        bucketname = 'AirDrum'
        self.s3.upload_file(filename, bucketname, filename)
