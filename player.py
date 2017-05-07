import json
import boto3
from multiprocessing.dummy import Pool

class player:
    def __init__(self, threads = 2):
        ##sqs
        sqs = boto3.resource('sqs')
        self.queue = sqs.get_queue_by_name(QueueName='######')

        ##multithread
        self.p = Pool(threads)

    def play(self):
        while(True):
            messages = self.queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20)
            print(str(len(messages)) + " messages from sqs")
            self.p.map(self.worker, messages)
    
    def worker(self, message):
        try:
            ##play music based on message from sqs
        except Exception as e:
            print e
        finally:
            message.delete()

if __name__ == '__main__':
    P = player()
    P.play