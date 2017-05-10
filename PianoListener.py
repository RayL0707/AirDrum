import sys,os
sys.path.insert(0, "LeapSDK/lib")
import Leap
import time,math



class PianoListener(Leap.Listener):

    def on_connect(self, controller):
        self.gest = [0,0,0,0,0]
        self.mod = 0
        self.switch = False
        self.f = open("piano.csv","w")
        self.finger_weight = [1.5, 1, 1.6, 1.7, 2.2]
        self.finger_weight1 = [1, 1, 1, 1, 1]
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
            #velocity check
            #cur_velo = math.sqrt(finger.tip_velocity[0] ** 2 + finger.tip_velocity[1] ** 2 + finger.tip_velocity[2] ** 2) if finger.tip_velocity[1] < 0 else -1
            cur_velo = finger.tip_velocity[1]
            cur_velo *= self.finger_weight[finger.type]
            if cur_velo < -160 and abs(cur_velo) > maxvel:
                largefin = finger.type
                maxvel = cur_velo
            line[finger.type] = str(cur_velo)

            # position check
            # cur_pos = finger.tip_position[1]
            # pos_diff = abs(calibrate_height[1] - cur_pos) * self.finger_weight[finger.type]
            # if pos_diff > maxvel:
            #     largefin = finger.type
            #     maxvel = pos_diff
            # line[finger.type] = str(pos_diff)

        res = ",".join(line)
        if largefin != -1:
            gest[int(largefin)] = 1
        self.gest = gest
        self.f.write(res + "," + '\n')
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
