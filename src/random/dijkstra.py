
import heapq

import numpy as np


def dijkstra_1(nodes, starting_node):
    large_number = 1e6
    distance = {key: large_number for key in nodes.keys()}
    distance[starting_node] = 0
    visited_nodes = set()
    priority_queue = [(0, starting_node)]
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node in visited_nodes:
            continue
        for node, value in nodes[current_node].items():
            new_distance = current_distance + value
            if new_distance < distance[node]:
                distance[node] = new_distance
                heapq.heappush(priority_queue, (new_distance, node))
        visited_nodes.add(current_node)

    return distance

def dijkstra_2(nodes, starting_node, distance_array):
    large_number = 1e6
    distance = {key: large_number for key in nodes.keys()}
    distance[*starting_node] = 0
    visited_nodes = set()
    priority_queue = [(0, starting_node)]
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node in visited_nodes:
            continue
        for node in nodes[*current_node]:
            new_distance = current_distance + distance_array[*node]
            try:
                if new_distance < distance[*node]:
                    distance[*node] = new_distance
                    heapq.heappush(priority_queue, (new_distance, node))
            except KeyError:
                distance[*node] = new_distance
        visited_nodes.add(current_node)

    return distance


def dijkstra_3(nodes, starting_node, distance_array):
    large_number = 1e6
    distance = np.full_like(distance_array, large_number, dtype=np.float32)
    distance[*starting_node] = 0
    visited_nodes = set()
    priority_queue = [(0, starting_node)]
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node in visited_nodes:
            continue
        for node in nodes[*current_node]:
            new_distance = current_distance + distance_array[*node]
            try:
                if new_distance < distance[*node]:
                    distance[*node] = new_distance
                    heapq.heappush(priority_queue, (new_distance, node))
            except KeyError:
                distance[*node] = new_distance
        visited_nodes.add(current_node)

    return distance


    # TODO

