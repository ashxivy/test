from graph import Graph, graph_from_file

class UnionFind:
    """
    Implementation of the Union-Find data structure with path compression.
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True


def kruskal1(graph):
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

    # création d'un dictionnaire qui contiendra l'arbre couvrant de poids minimal
    mst_graph = Graph()

    # Initialisation de la structure de données Union-Find
    uf = UnionFind(len(graph.nodes))

    # parcours des arêtes triées par poids croissant
    for power, node1, node2 in edges:
        # Si l'ajout de l'arête ne crée pas de cycle, on l'ajoute à l'arbre couvrant
        if uf.union(node1, node2):
            mst_graph.add_edge(node1, node2, power)

    return mst_graph


