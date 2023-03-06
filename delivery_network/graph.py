class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1
    

 
    

    def connected_components(self):
        liste_composantes = []
        noeuds_visites = {noeud: False for noeud in self.nodes}

        def visiter(noeud):
            composante = [noeud]
            for voisin in self.graph[noeud]:
                voisin = voisin[0]
                if not noeuds_visites[voisin]:
                    noeuds_visites[voisin]=True
                    composante += visiter(voisin)
            return composante

        for noeud in self.nodes:
            if not noeuds_visites[noeud]:
                liste_composantes.append(visiter(noeud))

        return liste_composantes



    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    


    def get_path_with_power(self, src, dest, power):
        """
        piste de doute: la condition sur la puissance du camion, actuellement implémentée dans la fonction find min
        possible que ça pose pb dans l'exploration de toutes les arrêtes 
        """

        test=False

        for liste in self.connected_components_set(): #on vérifie si les pt de départ et d'arrivé sont reliés pour savoir si un chemin existe
            if src and dest in liste:
                test=True

        if not test:
            chemin=None
        
        else: #programme si on sait qu'un chemin existe 

            #initialisation
            distance = {noeud: float('inf') for noeud in self.nodes}
            distance[src]=0
            origins = {noeud: None for noeud in self.nodes}
            liste_sommets=list(self.nodes)

            #définition des fonctions annexes
            def find_min(liste, power): #trouve le sommet le plus proche du pt de départ grâce au dico voisin avec la contrainte de puissance
                sol=0
                min_dist=float('inf')
                if liste is not None:
                    for sommet in liste:
                        for voisin in self.graph[sommet]:
                            if voisin[1]<=power:
                                if distance[voisin[0]] < min_dist:
                                    min_dist=distance[voisin[0]]
                                    sol = voisin[0]
                return sol
        
            def poids(s1,s2): #donne la distance entre deux points
                dist=None
                for voisin in self.graph[s1]:
                    if voisin[0]==s2:
                        dist=voisin[2]
                return dist

        
            def maj_dist(s1,s2): #met à jour les distances par rapport au point de départ et note l'antécédent du sommet considéré pour pouvoir faire le chemin inverse si un chemin est possible grâce au dico origins
                if distance[s2]>distance[s1] + poids(s1,s2):
                    distance[s2] = distance[s1] + poids(s1,s2)
                    origins[s2]=s1


            #programme principal qui associe à chaque sommet une distance par rapport au point de départ en tenant compte de la contrainte
            while liste_sommets != [] and liste_sommets is not None:
                point=find_min(liste_sommets,power)
                liste_sommets=liste_sommets.remove(point)
                for voisin in self.graph[point]:
                    maj_dist(point, voisin[0])

            #programme qui construit le plus court chemin
            chemin=[]
            s=dest
            while s != src:
                chemin +=[s]
                s=origins[s]
            chemin+=[src]
            chemin.reverse()
        
        return chemin
    



    def get_shorter_path(self, src, dest):
        
        test=False

        for liste in self.connected_components_set(): #on vérifie si les pt de départ et d'arrivé sont reliés pour savoir si un chemin existe
            if src and dest in liste:
                test=True

        if not test:
            chemin=None
        
        else: #programme si on sait qu'un chemin existe 

            #initialisation
            distance = {noeud: float('inf') for noeud in self.nodes}
            distance[src]=0
            origins = {noeud: None for noeud in self.nodes}
            liste_sommets=list(self.nodes)

            #définition des fonctions annexes
            def find_min(liste, power): #trouve le sommet le plus proche du pt de départ grâce au dico voisin avec la contrainte de puissance
                sol=0
                min_dist=float('inf')
                if liste is not None:
                    for sommet in liste:
                        for voisin in self.graph[sommet]:
                                if distance[voisin[0]] < min_dist:
                                    min_dist=distance[voisin[0]]
                                    sol = voisin[0]
                return sol
        
            def poids(s1,s2): #donne la distance entre deux points
                dist=None
                for voisin in self.graph[s1]:
                    if voisin[0]==s2:
                        dist=voisin[2]
                return dist

        
            def maj_dist(s1,s2): #met à jour les distances par rapport au point de départ et note l'antécédent du sommet considéré pour pouvoir faire le chemin inverse si un chemin est possible grâce au dico origins
                if distance[s2]>distance[s1] + poids(s1,s2):
                    distance[s2] = distance[s1] + poids(s1,s2)
                    origins[s2]=s1


            #programme principal qui associe à chaque sommet une distance par rapport au point de départ en tenant compte de la contrainte
            while liste_sommets != [] and liste_sommets is not None:
                point=find_min(liste_sommets,power)
                liste_sommets=liste_sommets.remove(point)
                for voisin in self.graph[point]:
                    maj_dist(point, voisin[0])

            #programme qui construit le plus court chemin
            chemin=[]
            s=dest
            while s != src:
                chemin +=[s]
                s=origins[s]
            chemin+=[src]
            chemin.reverse()
        
        return chemin




        
    









    
    def min_power(self, src, dest):
        path=self.get_shorter_path(self, src, dest)
        power=0
        for i in len(path):
            etape=path[i]
            for voisin in self.graph[etape]:
                if voisin[0]==path[i+1]:
                    if voisin[1]>power:
                        power=voisin[1]
        return path, power



def graph_from_file(filename):
    def graph_from_file(filename):
    f = open(filename,"r",encoding="utf-8")
    s = f.readlines()
    
    for i in range(0, len(s)): 
        s[i]=s[i].split(" ")
    
    for i in range(0, len(s)): 
        if len(s[i])<3:
            s[i][1]=int(s[i][1])
            s[i].append(1)
        else : 
            s[i][2]=int(s[i][2])
    g=Graph()
    print(s)
    for i in s:
        g.add_edge(i[0],i[1], i[2] )
    return g
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    g: Graph
        An object of the class Graph with the graph from file_name.
    """
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g
