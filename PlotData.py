import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# finger_fast = np.array(pd.read_csv("finger_fast.csv",header = None))
# finger_slow = np.array(pd.read_csv("finger_fast.csv",header = None))
# hand_fast = np.array(pd.read_csv("finger_fast.csv",header = None))
# hand_slow = np.array(pd.read_csv("finger_fast.csv",header = None))
raw_data = np.array(pd.read_csv("data.csv",header = None))
#print raw_data[:3]
print raw_data.shape
def getplot(data):
	xl = np.arange(0,len(data))

	#for i in range(3):
	plt.plot(xl,data[:,1].ravel(),label ='Velocity '+str(i))
	plt.title("V vs.t")
	plt.xlabel("time")
	plt.ylabel("speed")
	plt.legend(loc=0)
	plt.show()
getplot(raw_data)
