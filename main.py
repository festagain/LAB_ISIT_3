import AUTH
from pyvis.network import Network
import vk_api
import networkx as nx


# Авторизация в VK API

def two_factor():  # Двухфакторная аутентификация
    key = input("Enter authentication code: ")
    return key, True


def get_friends_ids(vk, user_id):
    try:
        friends_ids = vk.friends.get(user_id=user_id)['items']
        return friends_ids
    except Exception as e:
        print(f"Error: {e}")
        return []


login = AUTH.login
password = AUTH.password

vk_session = vk_api.VkApi(login, password, auth_handler=two_factor, app_id=2685278)
try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)

vk = vk_session.get_api()
user_id_group = [224364474, 256804252, 212487510, 531619927, 194848002, 381907905, 444639273, 308412461, 308412461,
                 232210943, 75785096, 112370537, 139939428, 54705450, 236783753, 146075397, 383087847, 146697287,
                 315590903, 461814307, 143661083, 260727197, 276581495, 163067034, 184267947]

nt = Network()
G = nx.Graph()
added_nodes = set()
for user in user_id_group:
    print(user)
    friends_ids = get_friends_ids(vk, user)[:50]
    if user not in added_nodes:
        nt.add_node(user, color="red")
        G.add_node(user)
        added_nodes.add(user)

    for friend_id in friends_ids:
        if friend_id not in added_nodes:
            nt.add_node(friend_id, color="green")
            G.add_node(user)
            added_nodes.add(friend_id)

        nt.add_edge(user, friend_id)
        G.add_edge(user, friend_id)

        friends_of_friend_ids = get_friends_ids(vk, friend_id)[:50]
        for foaf_id in friends_of_friend_ids:
            if foaf_id not in added_nodes:
                nt.add_node(foaf_id, color="blue")
                G.add_node(user)
                added_nodes.add(foaf_id)
            nt.add_edge(friend_id, foaf_id)
            G.add_edge(friend_id, foaf_id)

            # Проверяем друзей у foaf_id
            # friends_of_foaf_id = get_friends_ids(vk, foaf_id)

            # for friend_of_foaf in friends_of_foaf_id:
            #     if friend_of_foaf in added_nodes:  # если друг уже есть в графе
            #         nt.add_edge(foaf_id, friend_of_foaf)
print(f'Count edges: {nt.num_edges()}')
print(f'Count nodes: {nt.num_nodes()}')


def loop(characters: list, vary: str):
    for u in characters:
        if int(u[0]) in user_id_group:
            print(f'{vary} {u}')
            break


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

nt.save_graph("12.html")
