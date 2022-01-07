from create_visibility_graph import create_visibility_graph
from Figure import Figure

from queue import PriorityQueue
from math import inf


def dijkstra(graph, s, t):
    queue = PriorityQueue()

    d = {x: inf for x in graph.keys()}
    d[s] = 0
    parent = {x: None for x in graph.keys()}
    visited = {x: False for x in graph.keys()}

    i = 0
    queue.put((0, i, s))
    while not queue.empty():
        u = queue.get()[2]

        if visited[u]:
            continue

        visited[u] = True
        for v, edge_weight in graph[u].items():
            if not visited[v] and d[u] + edge_weight < d[v]:
                parent[v] = u
                d[v] = d[u] + edge_weight
                i += 1
                queue.put((d[v], i, v))

    path = []
    u = t
    while u is not None:
        path.append(u)
        u = parent[u]

    return d[t], path


def shortest_path(figures, s, t):
    figures.append(Figure([s]))
    figures.append(Figure([t]))

    vb = create_visibility_graph(figures)

    return dijkstra(vb.get_graph(), s, t)

