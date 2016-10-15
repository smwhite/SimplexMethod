import os
import numpy as np

filename = "TestGame.txt"
#############################################
def findpivot():
    global pivot
    fp = True
    pl =[]
    while(fp):
        px= 0
        py= 0
        for c in column:
            if c < 0:
                for i in data[:,px]:
                    if i != 0:
                        pl.append(row[py]/i)
                        py +=1
                    elif i == 0:
                        pl.append(1000)
                        py +=1
                
                        
                    
                fp =False
                break
            px +=1
    py= 0
    pivot = min(pl)

    for i in pl:
        if i == pivot:
            break
        py+=1
    pivot = data[px,py]
    return [px,py]
#############################################

def PivotCalculation():
    pivotData = data.copy()
    yl=0
    xl=0
    for y in pivotData:
        for x in y:
            #if pivot
            if xl == pivotPosition[0] and yl == pivotPosition[1]:
                pivotData[xl,yl] = 1/x

            #else if in pivot column
            elif yl == pivotPosition[1]:
                pivotData[xl,yl] = -data[xl,yl]/pivot
            #else if in pivot row
            elif xl == pivotPosition[0]:
                pivotData[xl,yl] = data[xl,yl]/pivot
            #else if in neither
            elif xl != pivotPosition[0] and yl != pivotPosition[1]:
                d= data[pivotPosition[0],yl]*data[xl,pivotPosition[1]]
                pivotData[xl,yl] = data[xl,yl]- (d/pivot)
            xl +=1
        yl+=1
        xl =0
    # calculation for borders 
    global row,column, brc
    newRow = row[:]
    newColumn = column[:]
    yl=0
    xl=0
    for x in row:
        if xl  == pivotPosition[1]:
            newRow[xl] = row[xl]/pivot
        else:
            d = row[pivotPosition[1]] * data[xl,pivotPosition[1]]
            newRow[xl] = row[xl] - (d/pivot)

        xl+=1
        
    for y in column:
        if yl == pivotPosition[0]:
            newColumn[yl] = - column[yl]/pivot
        else:
            d = column[pivotPosition[0]] * data[pivotPosition[0],yl]
            newColumn[yl] = column[yl] - (d/pivot)
            

        yl+=1

    brc -= row[pivotPosition[0]]*column[pivotPosition[1]] /pivot
    
    row = newRow[:]
    column = newColumn[:]
    return pivotData


#############################################

# start of Simplex solver


row = []
column = []
brc = 0
x = []
y = []
pivot = 0

data = np.loadtxt(os.path.abspath(filename))

dataNumRows = data.shape[0]
dataNumColumns = data.shape[1]


# initialize the "extra" rows and columns to the game size
i = 0
while (i<dataNumRows):
    x.append('x')
    row.append(1)
    i += 1


i = 0
while (i<dataNumColumns):
    y.append('y')
    column.append(-1)
    i += 1

lowestValue = data.min()
data = data + abs(lowestValue)
solve = True

while(solve):
    
    pivotPosition = findpivot()
    
    if pivot < 0:
        print "Something went wrong while selecting pivot"
        break
    else:
        print "pivot is ",pivot

    data = PivotCalculation().copy()

    x[pivotPosition[0]],y[pivotPosition[1]] = y[pivotPosition[1]],x[pivotPosition[0]]


    if min(column) > 0:
        solve = False

print data
print row
print column
print brc
print x
print y
print
print
print


# end results
vb = np.reciprocal(brc)
v = round(vb + lowestValue,2)
print "the value of the game is", v

P=[]
Q=[]
i=0

for x in x:
    if x == 'x':
        P.append(0)
    else:
        P.append(round(column[i]*vb,2))
    i+=1

print "the probability that player 1's choices will pay off are", P


i=0

for y in y:
    if y == 'y':
        Q.append(0)
    else:
        Q.append(round(row[i]*vb,2))
    i+=1

print "the probability that player 2's choices will pay off are", Q
