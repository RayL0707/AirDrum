import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# finger_fast = np.array(pd.read_csv("finger_fast.csv",header = None))
# finger_slow = np.array(pd.read_csv("finger_fast.csv",header = None))
# hand_fast = np.array(pd.read_csv("finger_fast.csv",header = None))
# hand_slow = np.array(pd.read_csv("finger_fast.csv",header = None))
raw_data = np.array(pd.read_csv("piano.csv",header = None))
#print raw_data[:3]
print raw_data
def getplot(data):
	x = np.arange(0,len(data))

	# for i in range(data.shape[1]):
	# 	plt.plot(xl,data[:,i].ravel(),label ='Finger '+str(i))
	# 	plt.title("V vs.t")
	# 	plt.xlabel("time")
	# 	plt.ylabel("speed")
	# 	plt.legend(loc=0)
	f, axarr = plt.subplots(5)
	for i in range(data.shape[1]):
		axarr[i].plot(x, data[:,i].ravel())
		axarr[i].set_title('Finger '+str(i + 1))
		plt.subplots_adjust(hspace = 0.5)
	plt.show()
getplot(raw_data)
