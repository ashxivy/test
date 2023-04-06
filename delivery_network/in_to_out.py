
from graph import Graph, graph_from_file
import math as mt

def fct_fichier_min_power(fileroute,filenetwork):

    f=open(fileroute, "r", encoding="utf-8")
    s=f.readlines()
    a=0
    b=mt.floor(mt.log(len(s)))
    L=[]
    for i in range(1, len(s)):
        s[i]=s[i].split(" ")
        s[i][1]=int(s[i][1])
        s[i][0]=int(s[i][0])
    g=graph_from_file(filenetwork)


    for i in range(1,len(s)):
        L.append(str(g.min_power(s[i][0], s[i][1])[1]))


    print(L)

    with open(fileroute[:-2]+"out", "w") as file:



        for item in L:

            file.write(item + "\n")

    

    file.close()





fct_fichier_min_power("input/routes.2.in", "input/network.2.in")



import os



print(os.path.abspath("input/routes.1.out")) 

