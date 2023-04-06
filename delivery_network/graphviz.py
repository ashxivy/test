import graphviz
from graph import Graph, graph_from_file





# Exemple de dictionnaire de graphique

graph_dict = graph_from_file("input/network.01.in")



# Créer un objet Digraph

graph = graphviz.Digraph()



# Ajouter les nœuds

for node in graph_dict.nodes:

    graph.node(node)



# Ajouter les arêtes

for node, edges in graph_dict.items():

    for edge in edges:

        neighbor, power, distance = edge

        # Ajouter une arête avec une étiquette pour la puissance et la distance

        graph.edge(node, neighbor, label=f"Power: {power}, Distance: {distance}")



# Rendu du graphique

graph.view()

"""graph.render('nom_du_fichier', format='png')"""