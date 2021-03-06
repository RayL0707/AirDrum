import sys,os
sys.path.insert(0, "LeapSDK/lib")
import Leap
<<<<<<< HEAD
import time,math
=======
import time, math
>>>>>>> Demobr



class PianoListener(Leap.Listener):

    def on_connect(self, controller):
        self.gest = [0,0,0,0,0]
        self.mod = 0
        self.switch = False
        # self.f = open("piano.csv","w")
        os.system('clear')
        print "Connected"
        print "Piano Mode"

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
            #print "Place One hand here for monitoring"
            #time.sleep(0.02)
            return
        if hand.palm_velocity[0] < -1000:
            self.switch = True
            return
        largefin = -1
        maxvel = 0
        gest = [0,0,0,0,0]
        calibrate_height = hand.palm_position
        #print calibrate_height
        line = [0,0,0,0,0]
        for i, finger in enumerate(fingers):
            cur_velo = math.sqrt(finger.tip_velocity[0] ** 2 + finger.tip_velocity[1] ** 2 + finger.tip_velocity[2] ** 2) if finger.tip_velocity[1] < 0 else 0
            if cur_velo > 175 and cur_velo > maxvel:
                largefin = finger.type
                maxvel = cur_velo


        if largefin != -1:
            gest[int(largefin)] = 1
        self.gest = gest
        #self.f.write(str(fingers[0].tip_velocity[1])+","+str(fingers[1].tip_velocity[1])+","+str(fingers[2].tip_velocity[1])+","+str(fingers[3].tip_velocity[1])+","+str(fingers[4].tip_velocity[1])+","+'\n')
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
