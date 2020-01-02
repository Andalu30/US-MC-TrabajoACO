'''  
3 data files

jobs became available at time zero
p(j) -> uninterrupted processing time
w(j) -> positive weight
d(j) -> due_date

C(j) -> Earliest completion time
T(j) -> max{C(j)-d(j), 0}


------------------instances------------
n=40,50,100

wt40, wt50, and wt100 containing the instances of size 40, 50, and 100 respectively

Each file contains the data for 125 instances, listed one after the other

The n processing times are listed first,
followed by the n weights,
and finally n due dates,

for each of the 125 instances in turn.
'''


import numpy as np
import sys

ProcessingTimes = [26, 24, 79, 46, 32, 35, 73, 74, 14, 67, 86, 46, 78, 40, 29, 94, 64, 27, 90, 55, 35, 52, 36, 69, 85, 95, 14, 78, 37, 86, 44, 28, 39, 12, 30 ,68 ,70 , 9, 49, 50]

Weights = [1, 10, 9, 10, 10, 4, 3, 2, 10, 3, 7, 3, 1, 3, 10, 4, 7, 7, 4, 7, 5, 3, 5, 4, 9, 5, 2, 8, 10, 4, 7, 4, 9, 5, 7, 7, 5, 10, 1, 3]

Due_dates = [1588,1620,1731,1773,1694,1487,1566,1844,1727,1636,1599,1539,1855,1645,1709,1660,1582,1836,1484,1559,1772,1510,1512,1795,1522,1509,1598,1658,1826,1628,1650,1833,1627,1528,1541,1497,1481,1446,1579,1814]

solucion = 913


pTime = []
for i, e in enumerate(ProcessingTimes):
    pTime.append(ProcessingTimes)

pTime = np.matrix(pTime)
np.fill_diagonal(pTime, 0)


weights = []
for i, e in enumerate(Weights):
    weights.append(Weights)

weights = np.matrix(weights)
np.fill_diagonal(weights, 0)


due_dates = []
for i, e in enumerate(Due_dates):
    due_dates.append(Due_dates)

due_dates = np.matrix(due_dates)
np.fill_diagonal(due_dates, 0)



#np.set_printoptions(threshold=sys.maxsize)


print(f'pTime = \n{pTime}')
print(f'weights= \n{weights}')
print(f'due_dates = \n{due_dates}')