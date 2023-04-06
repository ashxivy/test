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
        """
        but: déterminer les différentes composantes connexes du graphe.
        """
        liste_composantes = [] #on va faire une liste de liste de noeuds qui formeront une composante connexe
        noeuds_visites = {noeud: False for noeud in self.nodes} #on utilise un dictionnaire pour marquer si un noeud a été visité ou non

        def visiter(noeud):
            """
            but: à partir d'un noeud qui n'a pas été visité, on parcourt tout ses voisins, puis les voisins de ses voisins par récursivité 
            pour renvoyer une composante connexe à partir d'un noeud
            """
            composante = [noeud]
            for voisin in self.graph[noeud]: #on regarde les voisins du noeud considéré
                voisin = voisin[0]
                if not noeuds_visites[voisin]: #s'il n'a pas déjà été visité (càd ajouté à la liste d'une composante)
                    noeuds_visites[voisin]=True
                    composante += visiter(voisin) #on itère sur les voisins des voisins 
            return composante

        for noeud in self.nodes:
            if not noeuds_visites[noeud]: #tant que tous les noeuds ont pas été visités
                liste_composantes.append(visiter(noeud)) #on ajoute les composantes connexes une à une 

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

    def min_power(self,src,dest):
        """
        calcule, pour un trajet t donné, la puissance minimale d'un camion pouvant couvrir ce trajet. La fonction devra 
        retourner le chemin, et la puissance minimale.
        On utilise ici une approche par dichotomie 
        """
        min_power=0
        max_power=0
        for node in self.nodes: #d'abord on va chercher à déterminer qu'elle est la puissance maximale pour circuler sur le graph
            for voisin in self.graph[node]:
                if voisin[1]>max_power:
                    max_power=voisin[1]
        while max_power-min_power>1: #par dichotomie, on va déterminer la puissance minimale pour effectuer un trajet 
            if self.get_path_with_power(src,dest,min_power)==None:
                min_power=mt.floor((max_power+min_power)/2)-1
            else: 
                max_power=mt.floor((max_power+min_power)/2)

        return self.get_path_with_power(src,dest,min_power), min_power


    def min_power_kruskal(self,src,dest):
        """
        """
        g = kruskal(self)
        path=g.get_path_with_power(src,dest,float('inf'))
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
    """
    fonction kruskal qui prend en entrée un graphe au format de la classe Graph (e.g., g) et qui retourne un autre 
    élément de cette classe (e.g., g_mst) correspondant à un arbre couvrant de poids minimal de g. 
    Analyser la complexité de l'algorithme implémenté.
    Indice : On suggère d'implémenter l'algorithme de Kruskal. Celui-ci est très simple : on prend chaque
    arête dans l'ordre des poids croissant seulement si l'ajouter aux arêtes déjà prises ne crée pas de cycle
    (sinon on la jète et on passe à la suivante). La difficulté est de, quand on considère une arête, déterminer
    rapidement si l'ajouter aux arêtes déjà prises crée un cycle. Ceci peut être fait efficacement avec une
    structure de donnée particulière appelé Union-Find.
    """
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
        mst_graph.nb_nodes = len(mst_graph.nodes)
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

