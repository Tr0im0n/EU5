
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


def dijkstra_3(all_nodes, starting_node, distance_array):
    large_number = 1e6
    distance = np.full_like(distance_array, large_number, dtype=np.float32)
    distance[*starting_node] = 0
    visited_nodes = np.zeros_like(distance_array, dtype=np.int8)
    visited_nodes[(0, 19), :] = 1
    # visited_nodes[19, :] = 1
    visited_nodes[:, 0] = 1
    visited_nodes[:, 19] = 1

    priority_queue = [(0, starting_node)]
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if visited_nodes[*current_node]:
            continue
        for adjacent_node in all_nodes[*current_node]:
            new_distance = current_distance + distance_array[*adjacent_node]
            try:
                if new_distance < distance[*adjacent_node]:
                    distance[*adjacent_node] = new_distance
                    heapq.heappush(priority_queue, (new_distance, tuple(adjacent_node)))
            except KeyError:
                distance[*adjacent_node] = new_distance
        visited_nodes[current_node] = 1

    return distance

def dijkstra_multi(all_nodes, starting_nodes, distance_array):
    large_number = 1e6
    needed_shape = (*distance_array.shape, 2)
    distance = np.full(needed_shape, large_number, dtype=np.float32)
    for i, starting_node in enumerate(starting_nodes):
        distance[*starting_node] = 0, i

    visited_nodes = np.zeros(needed_shape, dtype=np.int8)
    visited_nodes[(0, 19), :, 0] = 1
    visited_nodes[:, (0, 19), 0] = 1

    priority_queue = [(0, i, starting_node) for i, starting_node in enumerate(starting_nodes)]
    while priority_queue:
        current_distance, start_node_index, current_node = heapq.heappop(priority_queue)
        if visited_nodes[*current_node, 0]:
            continue
        for adjacent_node in all_nodes[*current_node]:
            new_distance = current_distance + distance_array[*adjacent_node]
            """
            if (current_node == on_land) and (adjacent_node == on_sea):
                new distance += current node harbor cost
            elif (current_node == on_sea) and (adjacent_node == on_land):
                new distance += adjacent node harbor cost
            """
            try:
                if new_distance < distance[*adjacent_node, 0]:
                    distance[*adjacent_node] = new_distance, start_node_index
                    heapq.heappush(priority_queue, (new_distance, start_node_index, tuple(adjacent_node)))
            except KeyError:
                distance[*adjacent_node, 0] = new_distance
        visited_nodes[current_node] = 1

    return distance


    # TODO

