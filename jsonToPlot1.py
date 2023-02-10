#! /usr/bin/python

import csv
import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor,Button
from numpy import random
import pandas as pd
import numpy as np
import pandas
import json



n = len(sys.argv)

filename1=sys.argv[1]
filename2=sys.argv[2]

with open(filename1) as json_file:
    data = json.load(json_file)

timestamp =data["start"]["timestamp"]["timesecs"]
#print(timestamp)
intervals = data["intervals"]

data_file = open('result.csv', 'w')

csv_writer = csv.writer(data_file)

data = {}
csv_writer.writerow(("end","jitter_ms", "bits_per_second","lost_packets"))


for interval in intervals:
    stream_data = []
    sum_data = []
    streams = interval["streams"]
    for stream in streams:
        data["end"] = stream["end"] + timestamp
        data["bits_per_second"] = stream["bits_per_second"]/100
        data["jitter_ms"] = stream["jitter_ms"]
        data["lost_packets"] = stream["lost_packets"]
        stream_data.append(data)
   
    sum = interval["sum"]
    data["end"] = stream["end"] + timestamp
    data["bits_per_second"] = stream["bits_per_second"]/100
    data["jitter_ms"] = stream["jitter_ms"]
    data["lost_packets"] = stream["lost_packets"]
    sum_data.append(data)
    csv_writer.writerow((round(data["end"]),data["jitter_ms"],data["bits_per_second"],data["lost_packets"]))


data_file.close()

dict_from_csv = {}
with open('result.csv', mode='r') as inp:
    reader = csv.reader(inp)
    next(reader) # skips the first(header) lin
    dict_from_csv = {rows[0]:rows[2] for rows in reader}



with open(filename2) as json_file:
    data = json.load(json_file)

inter = data["timedrop"]
event_file = open('event.csv', 'w')

event_csv_writer = csv.writer(event_file)
event_csv_writer.writerow(("Time", "Event","Latency","Drop","Jitter"))

mapi={}

for dum in inter:
      mapi["Time"]=dum["Time"]
      mapi["Event"]=dum["Event"]
      mapi["Latency"]=dum["Latency"]
      mapi["Drop"]  = dum["Drop"]
      mapi["Jitter"]= dum["Jitter"]
      event_csv_writer.writerow((round(mapi["Time"]), mapi["Event"],mapi["Latency"],mapi["Drop"],mapi["Jitter"]))


event_file.close()



plt.style.use('bmh')

df= pd.read_csv("result.csv")


df1= pd.read_csv("event.csv")

x=df['end']
y=df['bits_per_second']



x1=df1['Time']
y1=df1['Event']
a2=df1['Latency']
b2=df1['Drop']
c2=df1['Jitter']


leng=len(a2)
allevents=[]
temp=""
for i in range(leng):
    temp= str(y1[i])+" , "+"Latency : "+ str(a2[i])+" , "+"Drop : "+str(b2[i])+" , "+"Jitter : "+str(c2[i])
    allevents.append(temp)
    temp=""


x_n=[]

for it in x1:
    x_n.append(it)


y_n=[]
for i in x1:
    y_n.append(dict_from_csv[str(i)])

res = [eval(i) for i in y_n]


def mouse_event(event):
    print('x: {} Sec and y: {} GB_per_second'.format(round(event.xdata,2), round(event.ydata/10000,2)))

fig = plt.figure()
cid = fig.canvas.mpl_connect('button_press_event', mouse_event)
#plt.axis(xmin=-1, xmax=10, ymin=0, ymax=40)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
#ax = fig.add_axes([-1, 10, 0, 40])
ax.scatter(x, y, c='red')
ax.scatter(x_n,res, c='darkblue')

ax.set_xlabel("Intervals (in sec)")
ax.set_ylabel("Bits (GB_per_second)")

temp=min(res)

for i,j ,k  in zip(x_n,res,allevents):
    if j<=temp :
        plt.text(i,j,k,fontsize=14,rotation=90,horizontalalignment='center')
    else :
        plt.text(i,j,k,fontsize=14,rotation=270, verticalalignment='top')


plt.title("Fig2:-Bits_per_sec vs Intervals", fontsize=12)
plt.plot(x,y,label='figure2')

cursor =Cursor(ax, horizOn=True, vertOn=True, color='blue', linewidth=0.5)



plt.show()
