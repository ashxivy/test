import time 
import math as mt
from graph import Graph, graph_from_file




def test_time_min_power(filename1,filename2):
    f=open(filename1, "r", encoding="utf-8")
    s=f.readlines()
    a=0
    b=mt.floor(mt.sqrt(len(s)))
    for i in range(1, b):
        s[i]=s[i].split(" ")
        s[i][1]=int(s[i][1])
        s[i][0]=int(s[i][0])
    g=graph_from_file(filename2)
        
    t0=time.perf_counter()

    for i in range(1,b):
        g.min_power(s[i][0], s[i][1])
    
    t1=time.perf_counter()

    return ((t1-t0)*len(s)/b)


print(test_time_min_power("input/routes.2.in", "input/network.2.in"))



def test_time_min_power_kruskal(filename1,filename2):
    f=open(filename1, "r", encoding="utf-8")
    s=f.readlines()
    a=0
    b=mt.floor(mt.log(len(s)))
    for i in range(1, len(s)):
        s[i]=s[i].split(" ")
        s[i][1]=int(s[i][1])
        s[i][0]=int(s[i][0])
        s[i][2]=int(s[i][2])
    
    g=graph_from_file(filename2)


    t0=time.perf_counter()
    for i in range(1,11):
        g.min_power_kruskal(s[i][0], s[i][1])
    
    t1=time.perf_counter()

    return ((t1-t0)*len(s)/10)

print(test_time_min_power_kruskal("input/routes.2.in", "input/network.2.in"))