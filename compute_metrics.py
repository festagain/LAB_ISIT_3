import networkx as nx
import edges
import csv

nodes = set()
G = nx.Graph()
user_id_group = [224364474, 256804252, 212487510, 531619927, 194848002, 381907905, 444639273, 308412461, 308412461,
                 232210943, 75785096, 112370537, 139939428, 54705450, 236783753, 146075397, 383087847, 146697287,
                 315590903, 461814307, 143661083, 260727197, 276581495, 163067034, 184267947]

for el in edges.edge_dict:
    nodes.add(el['from'])

for el in nodes:
    G.add_node(el)

for el in edges.edge_dict:
    G.add_edge(el['from'], el['to'])

def loop(characters: list, vary: str):
    for u in characters:
        if int(u[0]) in user_id_group:
            print(f'{vary} {u}')
            break

# with open('cosmocsv.csv', "w") as f:
#     writer = csv.writer(f, delimiter=",", lineterminator="\r\n")
#     writer.writerows(edge)


characters_degree = sorted(list(nx.degree_centrality(G).items()), key=lambda i: i[1], reverse=True)
loop(characters_degree, 'Degree')

characters_closest = sorted(list(nx.closeness_centrality(G).items()), key=lambda i: i[1], reverse=True)
loop(characters_closest, 'Closest')

characters_vectors = sorted(list(nx.eigenvector_centrality(G).items()), key=lambda i: i[1], reverse=True)
loop(characters_vectors, 'Vector')

characters_mediation = sorted(list(nx.betweenness_centrality(G).items()), key=lambda i: i[1], reverse=True)
loop(characters_mediation, 'Mediation')

characters_pagerank = sorted(list(nx.pagerank(G, alpha=0.85).items()), key=lambda i: i[1], reverse=True)
loop(characters_pagerank, 'PageRank')