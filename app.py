import sys
sys.path.insert(0, "LeapSDK/lib")
import Leap
import time



class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        self.gest = [0,0,0,0]
        self.f = open("data.csv","w")
        self.rvelo = None
        self.lvelo = None
        self.lpos = None
        self.rpos = None
        print "Connected"

    def on_frame(self, controller):
        frame = controller.frame()
        if len(frame.hands) ==2:
            hands = frame.hands
            # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            # frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))
            if hands[0].is_left:
                lhand = hands[0]
                rhand = hands[1]
            else:
                lhand = hands[1]
                rhand = hands[0]
            hands = frame.hands
        else:
            print "Place your two hand here for monitoring"
            time.sleep(0.2)
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
        if self.rvelo[1] < -800:
            if self.rpos[2] > 0:
                tempgest[2] = 1
                # print "Top Right Hit!"
            else:
                tempgest[3] = 1
                #print "Down Right Hit!"
        if self.lvelo[1] < -800:
            if self.lpos[2] > 0:
                tempgest[0] = 1
            else:
                tempgest[1] = 1
        
        self.gest = tempgest
        self.f.write(str(self.lvelo[0])+","+str(self.lvelo[1])+","+str(self.lvelo[2])+","+str(self.lpos[0])+","+str(self.lpos[1])+","+str(self.lpos[2])+","+'\n')


# def main():
#     # Create a sample listener and controller
#     listener = SampleListener()
#     controller = Leap.Controller()

#     # Have the sample listener receive events from the controller
#     controller.add_listener(listener)

#     # Keep this process running until Enter is pressed
#     print "Press Enter to quit..."

#     try:
#         sys.stdin.readline()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         # Remove the sample listener when done
#         controller.remove_listener(listener)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        f.close()
        exit
