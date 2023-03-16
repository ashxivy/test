import graphviz
import math as mt

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
        Détermine si un camion de puissance p peut couvrir le trajet t,
        et retourne un chemin admissible si c'est possible, ou None sinon.
        """
        # Recherche en largeur du graphe pour trouver un chemin de s à t
        queue = [(src, [])]  # (sommet, chemin)
        visited = set()
        while queue: #tant que queue est non vide
            node, path = queue.pop(0)
            """
            L'instruction queue.pop(0) supprime et retourne le premier élément de la liste queue. 
            Dans ce cas, la variable node prend la valeur du premier élément de la liste, 
            qui est un tuple contenant le sommet courant, et la liste path qui contient le chemin parcouru pour arriver à ce sommet. 
            Ainsi, à chaque itération de la boucle while, on considère le prochain sommet de la queue pour explorer ses voisins.
            """
            if node == dest:  # Nous avons trouvé un chemin de src à dest
                return path + [dest]  # Ajouter le dernier sommet à la fin du chemin
            visited.add(node) #on ajoute node à la liste des sommets visités
            for voisin in self.graph[node]:
                if voisin[0] not in visited and voisin[1] <=  power:  # Nous ne visitons que les sommets avec des arêtes valides
                    queue.append((voisin[0], path + [node]))  # Ajouter le chemin à la liste de chemins pour le reparcourir
        # Si nous sortons de la boucle while sans trouver de chemin, cela signifie que nous n'avons pas trouvé de chemin valide
        return None
    """
    Question 6: complexité
    La fonction get_path_with_power est une recherche en largeur où on explore les sommets puis les arrêtes de ces sommets 
    un à un donc la complexité de l'algorythme dépend du graph sur lequel on travaille (sa taille)
    donc la complexité peut se résumer par O(|S|+|A|) avec S le nb de sommets et A le nb d'arrêtes. 
    """



    
    def find_all_paths(self, src, dest, path=[]):
        """
        Renvoie tous les chemins entre src et dest 
        """
        test=False

        for liste in self.connected_components_set(): #on vérifie si les pt de départ et d'arrivé sont reliés pour savoir si un chemin existe
            if src and dest in liste:
                test=True

        if not test:
            paths=None
        
        else: #programme si on sait qu'un chemin existe 
            if src == dest: #si on parvient jusqu'à la dernière arrête
                return [path + [src]]

            paths = []
            for node in self.graph[src]:
                if node[0] not in path: #on verifie si le sommet n'est aps déjà dans le chemin pour éviter les cycles
                    newpaths = self.find_all_paths(node[0], dest, path + [src]) 
                    for newpath in newpaths:
                        paths.append(newpath)

        return paths
    
    def min_power(self,src,dest):
        min_power=0
        max_power=0
        for node in self.nodes:
            for voisin in self.graph[node]:
                if voisin[1]>max_power:
                    max_power=voisin[1]
        while abs(max_power-min_power)>1:
            if self.get_path_with_power(src,dest,min_power)==None:
                min_power=mt.floor((max_power+min_power)/2)-1
            else: 
                max_power=mt.floor((max_power+min_power)/2)

        return self.get_path_with_power(src,dest,min_power), min_power



    def min_power_long(self, src, dest):
        """
        Écrire une fonction min_power qui calcule, pour un trajet t donné, la puissance minimale
        d’un camion pouvant couvrir ce trajet. La fonction devra retourner le chemin, et la puissance minimale.
        """
        paths = self.find_all_paths(src, dest) #on receuille tous les chemins possibles
        powers = []

        def get_power(path): #on définit une fonction qui calcule la puissance nécéssaire pour parcourir un chemin
            power = 0
            for i in range(len(path)-1):
                for voisin in self.graph[path[i]]:
                    if voisin[0] == path[i+1] and voisin[1]>power:
                        power = voisin[1]
            return power

        for path in paths:
            powers.append(get_power(path)) #on receuille la puissance nécéssaire de tous les chemins

        power = min(powers) #on prend le min des puissances
        i = powers.index(power)
        solution = paths[i] #on receuille le chemin qui nécéssite le moins de puissance

        return solution, power
    """
    Question 6: complexité

    Pour calculer la complexité de la fonction min_power on est obligé de considérer
    la complexité de la fonction find all path auquel on fait appel. 
    La fonction find_all_path peut être d'une très grande complexité de l'ordre de l'exponentielle 
    en fonction du nb de chemins possibles. Au pire des cas, sa complexité est donc de l'ordre de
    O(2^|A|) où |A| est le nombre d'arêtes dans le graphe. 
    
    La fonction find_min, calcule la puissance nécessaire  pour chaque chemin trouvé par find_all_paths. 
    Cette boucle itère à travers tous les chemins retournés par find_all_paths et pour chaque chemin elle itère à travers 
    toutes les arêtes de ce chemin pour trouver l'arête ayant la puissance maximale. La complexité de cette boucle est donc 
    O(P * L) où P est le nombre de chemins retournés par find_all_paths et L est la longueur maximale d'un chemin.

    donc la complexité finale est O(2^|A| + P * L)

    """
    

   


    
    def min_power_kruskal(self, src, dest):
        g = kruskal(self)

        def dfs(graph, src, dest, visited, origin):
            visited[src] = True
            for voisin in graph.graph[src]:
                origin[voisin[0]] = src
                if voisin[0] == dest:
                    path = [voisin[0]]
                    while path[0] != src:
                        path.insert(0, origin[path[0]])
                    return path
                elif not visited[voisin[0]]:
                    path = dfs(graph, voisin[0], dest, visited, origin)
                    if path is not None:
                        path.insert(0, src)
                        return path
            return None

        visited = {noeud: False for noeud in g.nodes}
        origin = {noeud: None for noeud in g.nodes}
        path = dfs(g, src, dest, visited, origin)

        def get_power(path): #on définit une fonction qui calcule la puissance nécéssaire pour parcourir un chemin
            power = 0
            for i in range(len(path)-1):
                for voisin in self.graph[path[i]]:
                    if voisin[0] == path[i+1] and voisin[1] > power:
                        power = voisin[1]
            return power

        return get_power(path), path
    """
    L'algorithme de Kruskal a une complexité de O(E log E), où E est le nombre d'arêtes du graphe.

    Ensuite, la fonction dfs est appelée pour trouver le chemin le plus court entre src et dest dans l'arbre de recouvrement minimum. 
    La complexité de dfs est O(E), car elle visite chaque arête une fois.

    Enfin, la fonction get_power est appelée pour calculer la puissance minimale nécessaire pour parcourir le chemin trouvé. 
    Cette fonction a une complexité de O(N^2), où N est le nombre de sommets du graphe, car elle doit parcourir toutes les arêtes 
    adjacentes à chaque sommet dans le chemin.

    Ainsi, la complexité totale de min_power_kruskal est de O(E log E + E + N^2), où E est le nombre d'arêtes du graphe et 
    N est le nombre de sommets du graphe.
    """

    

    


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




def kruskal(graph):
    # création d'une liste qui contiendra les arêtes triées par poids croissant
    edges = []
    for node in graph.nodes:
        for voisin in graph.graph[node]:
            edges.append((voisin[1], node, voisin[0])) #on met power en argument 1 pour que sort() l'ordonne 
    edges.sort()

    # création d'une liste qui contiendra les ensembles de noeuds connectés
    node_sets = []
    for node in graph.nodes:
        node_sets.append({node})

    # création d'un dictionnaire qui contiendra l'arbre couvrant de poids minimal
    mst_graph = Graph()

    # parcours de toutes les composantes connexes du graphe
    for component in graph.connected_components():
        # on réinitialise les listes et dictionnaires pour chaque composante connexe
        node_sets = []
        for node in component:
            node_sets.append({node})
        mst_graph.nodes = list(component)
        mst_graph.graph = {node: [] for node in component}

        # parcours des arêtes triées par poids croissant
        for power, node1, node2 in edges:
            # recherche des ensembles auxquels appartiennent node1 et node2
            node1_set = None
            node2_set = None
            for s in node_sets:
                if node1 in s:
                    node1_set = s
                if node2 in s:
                    node2_set = s
            # si les noeuds ne sont pas dans le même ensemble, alors l'arête est ajoutée à l'arbre couvrant
            if node1_set != node2_set:
                mst_graph.add_edge(node1, node2, power)
                # fusion des ensembles
                node1_set.update(node2_set)
                node_sets.remove(node2_set)
            # arrêt de la boucle si tous les noeuds appartiennent au même ensemble
            if len(node_sets) == 1:
                break

    return mst_graph

"""
La complexité de l'algorithme de Kruskal implémenté ici est de O(m log n), où n est le nombre de nœuds dans le graphe et m est le 
nombre d'arêtes dans le graphe. La complexité de la création de la liste des arêtes triées est de O(m log m) en raison du tri, mais 
étant donné que m est au maximum de l'ordre de n^2, cela revient à O(n^2 log n^2) = O(n^2 log n), qui est la même complexité que la 
fusion et la recherche d'ensemble dans la boucle principale. La création d'une nouvelle instance de la classe Graph dans la boucle 
principale peut également avoir une complexité linéaire en n, mais cela n'affecte pas la complexité globale de l'algorithme.
"""



import time 




def test_time_min_power(filename1,filename2):
    f=open(filename1, "r", encoding="utf-8")
    s=f.readlines()
    a=0
    b=mt.floor(mt.log(len(s)))
    for i in range(1, len(s)):
        s[i]=s[i].split(" ")
        s[i][1]=int(s[i][1])
        s[i][0]=int(s[i][0])
    g=graph_from_file(filename2)
        
    t0=time.perf_counter()

    for i in range(1,2):
        g.min_power(s[i][0], s[i][1])
    
    t1=time.perf_counter()

    return ((t1-t0)*len(s))


print(test_time_min_power("input/routes.1.in", "input/network.1.in"))


"""
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

print(test_time_min_power_kruskal("input/routes.1.in", "input/network.1.in"))
"""