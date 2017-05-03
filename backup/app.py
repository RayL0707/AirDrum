import sys
sys.path.insert(0, "LeapSDK/lib")
import Leap
import time



class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        self.gest = [0,0,0,0]
        print "Connected"


    def on_frame(self, controller):
        frame = controller.frame()
        self.gest = [0,0,0,0]
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

        rvelo = rhand.palm_velocity
        rpos = rhand.palm_position
        lvelo = lhand.palm_velocity
        lpos = lhand.palm_position
            # print "Right hand: " + str(rpos)
            # print "Left hand: "+ str(lpos)
        if rvelo[1] < -600:
            if rpos[1] > 250:
                self.gest[2] = 1
                # print "Top Right Hit!"
            else:
                self.gest[3] = 1
                #print "Down Right Hit!"
        if lvelo[1] < -600:
            if lpos[1] > 250:
                self.gest[0] = 1
            else:
                self.gest[1] = 1


    # def main(self):
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
        a = SampleListener()
        a.main()
    except KeyboardInterrupt:
        exit