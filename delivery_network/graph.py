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
    

    def get_path_with_power(self, src, dest, power):
        ensemble_chemins=[]
        resultat = []
        noeuds_visites = {noeud: False for noeud in self.nodes} #on marque tous les noeuds comme non visistés
        noeuds_visites[src]=True #on marque le sommet comme visité 
        point = src

        def passage(noeud): #on définit un pt de départ
            chemin = [noeud] 
            for voisin in self.graph[noeud]: #pour tous les voisins du points de départ
                if voisin[1]>power: #si ils ne sont pas accessibles
                    noeuds_visites[voisin]=None
                if voisin[1]<=power: #s'il sont accessibles 
                    voisin = voisin[0] 
                    if not noeuds_visites[voisin]: #s'ils n'ont pas été visistés 
                        noeuds_visites[voisin]=True #on les marque comme atteints
                        if voisin != dest: #s'ils sont différents du pt d'arrivé chercher, on les parcourt de même
                            chemin += passage(voisin)
                        else:
                            chemin += [dest]
                        break
            return chemin

        while False in noeuds_visites.values():
            ensemble_chemins += passage(src)

        for voie in ensemble_chemins:
            if voie[-1]==dest:
                resultat = voie
        if resultat == []:
            resultat = None

        return resultat



    

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
    
    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        raise NotImplementedError


def graph_from_file(filename):
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
