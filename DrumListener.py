import sys,os
sys.path.insert(0, "LeapSDK/lib")
import Leap
import time



class DrumListener(Leap.Listener):

    def on_connect(self, controller):
        self.gest = [0,0,0,0]
        # self.f = open("data.csv","w")
        self.rvelo = None
        self.lvelo = None
        self.lpos = None
        self.rpos = None
        self.switch = False
        os.system('clear')
        print "Connected"
        print "Drum Mode"

    def on_frame(self, controller):
        frame = controller.frame()
        if len(frame.hands) ==2:
            hands = frame.hands
            if hands[0].is_left:
                lhand = hands[0]
                rhand = hands[1]
            else:
                lhand = hands[1]
                rhand = hands[0]
            hands = frame.hands
        else:
            #print "Place your two hand here for monitoring"
            time.sleep(0.02)
            return
        if lhand.palm_velocity[0] > 1000:
            self.switch = True
            return
        rfrontfin = rhand.fingers.frontmost
        lfrontfin = lhand.fingers.frontmost
        self.rvelo = rfrontfin.tip_velocity
        self.lvelo = lfrontfin.tip_velocity
        #rvelo = rhand.palm_velocity
        self.rpos = rhand.palm_position
        #lvelo = lhand.palm_velocity
        self.lpos = lhand.palm_position
            # print "Right hand: " + str(rpos)
            # print "Left hand: "+ str(lpos)
        tempgest = [0,0,0,0]
        if self.rvelo[1] < -400:
            if self.rpos[2] > 0:
                tempgest[2] = 1
                # print "Top Right Hit!"
            else:
                tempgest[3] = 1
                #print "Down Right Hit!"
        if self.lvelo[1] < -400:
            if self.lpos[2] > 0:
                tempgest[0] = 1
            else:
                tempgest[1] = 1

        self.gest = tempgest

        #self.f.write(str(self.lvelo[0])+","+str(self.lvelo[1])+","+str(self.lvelo[2])+","+str(self.lpos[0])+","+str(self.lpos[1])+","+str(self.lpos[2])+","+'\n')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        f.close()
        exit
