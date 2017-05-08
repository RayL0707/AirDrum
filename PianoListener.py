import sys
sys.path.insert(0, "LeapSDK/lib")
import Leap
import time



class PianoListener(Leap.Listener):

    def on_connect(self, controller):
        self.gest = [0,0,0,0,0]
        self.mod = 0
        print "Connected"

    def on_frame(self, controller):
        frame = controller.frame()
        if len(frame.hands) ==1 and len(frame.hands[0].fingers) == 5:
            hand = frame.hands[0]
            fingers = frame.hands[0].fingers
            # thumb = fingers.fingerType(0).get(0)
            # index = fingers.fingerType(1).get(0)
            # middle = fingers.fingerType(2).get(0)
            # ring = fingers.fingerType(3).get(0)
            # pinky = fingers.fingerType(4).get(0)
        else:
            print "Place One hand here for monitoring"
            time.sleep(0.02)
            return
        largefin = -1
        maxvel = 0
        gest = [0,0,0,0,0]
        for finger in fingers:
            if finger.tip_velocity[1] <-200 and abs(finger.tip_velocity[1]) > maxvel:
                largefin = finger.type
        if largefin != -1:
            gest[int(largefin)] = 1
        self.gest = gest
        #print gest
        # self.thumbvel = thumb.tip_velocity
        # self.indexvel = index.tip_velocity
        # self.middlevel = middle.tip_velocity
        # self.ringvel = ring.tip_velocity
        # self.pinkyvel = pinky

if __name__ == "__main__":
    try:
        piano = PianoListener()
        controller = Leap.Controller()
        controller.add_listener(piano)
        while True:
            pass
    except KeyboardInterrupt:
        exit
