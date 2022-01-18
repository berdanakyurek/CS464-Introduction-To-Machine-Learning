from math import tan, sqrt

# 2.3
step = 0.1

from pandas import *
import numpy as np
data = []

reader = read_csv('question-2-features.csv')
lstat_col = reader['LSTAT'].tolist()

reader = read_csv('question-2-labels.csv')
prices = reader['Price'].tolist()
#print(prices)

def distance_to_line(a, b, c, x0, y0):

    y = a*x0 + c
    dif = y-y0
    if dif < 0:
        dif *= -1
    return dif


def SSdistance(lstat_col, prices, mean_lstat, mean_price, degree):
    slope = tan(degree)
    a = slope
    b = -1
    c = mean_price - slope * mean_lstat
    sum = 0
    for i in range(len(lstat_col)):
        sum += distance_to_line(a,b,c, lstat_col[i], prices[i])**2
    return sum

mean_lstat = sum(lstat_col)/len(lstat_col)
mean_price = sum(prices)/len(prices)
degree = 0

current = SSdistance(lstat_col, prices, mean_lstat, mean_price, degree)

increase = 0
if SSdistance(lstat_col, prices, mean_lstat, mean_price, degree+step) < current:
    increase = 1
elif SSdistance(lstat_col, prices, mean_lstat, mean_price, degree-step) < current:
    increase = -1

if increase != 0:
    while True:
        newres = SSdistance(lstat_col, prices, mean_lstat, mean_price, degree + increase * step)
        if newres > current:
            break
        current = newres
        degree += increase * step


import matplotlib.pyplot as plt

plt.scatter(lstat_col, prices)

slope = tan(degree)
x = np.linspace(0,40,1000)
c = mean_price - slope * mean_lstat
y = slope*x+c
plt.plot(x, y, '-r', label='y=2x+1')
plt.show()

print("%fx+%fy+%f=0 line"%(slope,-1,c))
