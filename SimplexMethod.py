import os
import numpy as np

row = [1,1,1]
column = [-1,-1,-1]
brc = 0

data = np.loadtxt(os.path.abspath("TestGame.txt"))

lowestValue = data.min()

data = data + abs(lowestValue)


findpivot(data)




def findpivot(data):
    pass
