from graph import Graph, graph_from_file

def glouton(filegraph, fileroute, filetruck):
    g=graph_from_file(filegraph)

    f=open(fileroute, "r", encoding="utf-8")
    s=f.readlines()
    route=[]
    for i in range(1, len(s)):
        s[i]=s[i].split(" ")
        route.append([int(s[i][2]),int(s[i][0]),int(s[i][1])]) #profit, départ, arrivée
    route.sort(reverse=True)
   

    t=open(filetruck, "r", encoding="utf-8")
    truck=t.readlines()
    trucks=[]
    for i in range(1, len(truck)):
        truck[i]=truck[i].split(" ")
        trucks.append([int(truck[i][0]),int(truck[i][1])]) #puissance et coût
        trucks.sort()
    
    def sort_trucks(trucks):
        for i in range(0,(len(trucks)-2)): #on met -2 car naturellement, la len rajoute 1 pour obtenir la bonne longueur dans une boucle in range, donc étant donné qu'on utilise i+1, il faut faire -1 en plus
            if trucks[i+1][1]<=trucks[i][1]:
                trucks.remove(trucks[i])
        return trucks
    
    trucks=sort_trucks(trucks)

    def coeff_advantage(g, route, trucks):
        for i in range (len(route)):
            min_power, path = g.min_power_kruskal(route[i][1],route[i][2])
            test=True
            while test:
                for j in range(len(trucks)):
                    if trucks[j][0]>=min_power:
                        route[i][0]=route[i][0]/trucks[j][1] #on divise le profit par le coût de revient
                        route[i]+=[path,j]#on ajoute l'indice du camion qu'il faudra prendre pour le retrouver facilement par la suite lors des calculs
                        test=False
                        break
        route.sort(reverse=True)
        return route
    
    route=coeff_advantage(g,route,trucks)
            
    budget=25*(10**9)
    spend=0
    results=[]

    while spend < budget:
        for i in range(len(route)):
            spend=spend + trucks[route[i][4]][1]
            results+=[[route[i][4],route[i][3]]] #l'indice du camion acheté + le chemin qu'il va réaliser
    
    if spend>budget:
        results.remove(results[-1])

    return results

print(glouton("input/network.2.in", "input/routes.2.in", "input/trucks.0.in"))