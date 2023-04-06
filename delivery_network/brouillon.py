from graph import Graph, graph_from_file

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


def min_power_kruskal_long(self, src, dest):
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