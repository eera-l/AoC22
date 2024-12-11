from collections import defaultdict, deque

import numpy as np

from itertools import permutations


class Valve:

    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.visited = False
        self.distance = 0
        self.is_open = False

    def set_visited(self, visited):
        self.visited = visited

    def set_open(self):
        self.is_open = True

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f'Valve {self.name} with rate {self.rate}. Neighbors: {self.neighbors}'

    def __repr__(self):
        return self.name


def parse_lines(lines):
    valves = []

    for line in lines:
        first, second = line.split(';')
        firsts = first.split()
        valve_name = firsts[1]
        valve_rate = int(firsts[4].split('=')[1])
        valves.append(Valve(valve_name, valve_rate))
    return valves


def add_neighbors(lines, valves):
    for line in lines:
        first, second = line.split(';')
        firsts = first.split()
        valve_name = firsts[1]

        try:
            neighbors = second.split('valves ')[1].split(', ')
        except IndexError:
            neighbors = second.split('valve ')[1]
        curr_valve = next(obj for obj in valves if obj.name == valve_name)
        curr_neighbors = []

        if isinstance(neighbors, str):
            n_valve = next((obj for obj in valves if obj.name == neighbors), None)
            if n_valve:
                curr_neighbors.append(n_valve)
        else:
            for neighbor in neighbors:
                n_valve = next((obj for obj in valves if obj.name == neighbor), None)
                if n_valve:
                    curr_neighbors.append(n_valve)
        curr_valve.set_neighbors(curr_neighbors)


def initialize_matrix(valves):
    dist_matrices = np.ndarray(shape=(len(valves), len(valves)))

    for i, valve in enumerate(valves):
        for j, n in enumerate(valves):
            if i == j:
                dist_matrices[i][j] = 0
            else:
                if n in valve.neighbors:
                    dist_matrices[i][j] = 1
                else:
                    dist_matrices[i][j] = np.inf
    return dist_matrices


def run_floyd_warshalls(valves, dist_matrices):
    n = len(valves)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist_matrices[i][j] = min(dist_matrices[i][j],
                                          dist_matrices[i][k] + dist_matrices[k][j])
    return dist_matrices


def name_to_idx(valves):
    n_dict = defaultdict(int)
    i_dict = defaultdict(str)

    for idx, node in enumerate(valves):
        n_dict[node.name] = idx
        i_dict[idx] = node.name

    return n_dict, i_dict


def prune_paths_2(valves, dist_matrices, n_dict):
    paths = []
    sum_paths = []
    permsf = list(permutations(valves[1:]))
    perms = [p for p in permsf if p[0].name == valves[0].name]

    for perm in perms:
        path = [perm[0]]
        sum_path = 0
        for idx in range(len(perm) - 1):
            i = n_dict[perm[idx].name]
            j = n_dict[perm[idx + 1].name]
            path.append(perm[idx + 1])
            sum_path += dist_matrices[i][j]
        if sum_path <= 28:
            paths.append(path)
            sum_paths.append(sum_path)

    return paths, sum_paths


def loop_through(paths, dist_matrices, n_dict):
    rates = []
    released_pressures = []
    for path in paths[:5]:
        print([n for n in path])
        pressure = 0
        p_rate = 0
        time_elapsed = 1
        for idx in range(len(path) - 1):
            print(f'1. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
            print(f'Node {path[idx].name}. Rate: {p_rate}')
            i = n_dict[path[idx].name]
            j = n_dict[path[idx + 1].name]
            if time_elapsed >= 30:
                break
            elif time_elapsed + dist_matrices[i][j] >= 30:
                time_left = 30 - time_elapsed - 1
                pressure += p_rate * time_left
                time_elapsed = 30
                print(f'b. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
            if path[idx].rate > 0:
                if time_elapsed < 30:
                    time_elapsed += 1
                    p_rate += path[idx].rate
                    pressure += p_rate
                    print(f'2. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
            if time_elapsed >= 30:
                break
            elif time_elapsed + dist_matrices[i][j] >= 30:
                time_left = 30 - time_elapsed - 1
                pressure += p_rate * time_left
                time_elapsed = 30
                print(f'3. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
            else:
                pressure += p_rate * dist_matrices[i][j]
                time_elapsed += dist_matrices[i][j]
                print(f'4. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
                if idx == len(path) - 2:
                    if path[idx + 1].rate > 0:
                        if time_elapsed < 30:
                            time_elapsed += 1
                            p_rate += path[idx + 1].rate
                            pressure += p_rate
                            print(f'5. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
                    if time_elapsed < 30:
                        time_left = 30 - time_elapsed - 1
                        pressure += p_rate * time_left
                        time_elapsed = 30
                        print(f'6. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
        rates.append(p_rate)
        released_pressures.append(pressure)
        print()
    return rates, released_pressures


def loop_through_prod(paths, dist_matrices, n_dict):
    rates = []
    released_pressures = []
    for path in paths:
        pressure = 0
        p_rate = 0
        time_elapsed = 1
        for idx in range(len(path) - 1):
            #print(f'1. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
            i = n_dict[path[idx].name]
            j = n_dict[path[idx + 1].name]
            if time_elapsed >= 30:
                break
            if path[idx].rate > 0:
                if time_elapsed < 30:
                    time_elapsed += 1
                    p_rate += path[idx].rate
                    pressure += p_rate
                    #print(f'2. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
            if time_elapsed >= 30:
                break
            elif time_elapsed + dist_matrices[i][j] >= 30:
                time_left = 30 - time_elapsed
                pressure += p_rate * time_left
                time_elapsed = 30
                #print(f'3. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
            else:
                pressure += p_rate * dist_matrices[i][j]
                time_elapsed += dist_matrices[i][j]
                #print(f'4. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
                if idx == len(path) - 2:
                    if path[idx + 1].rate > 0:
                        if time_elapsed < 30:
                            time_elapsed += 1
                            p_rate += path[idx + 1].rate
                            pressure += p_rate
                            #print(f'5. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
                    if time_elapsed < 30:
                        time_left = 30 - time_elapsed
                        pressure += p_rate * time_left
                        time_elapsed = 30
                        #print(f'6. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
        rates.append(p_rate)
        released_pressures.append(pressure)
        #print()
    return rates, released_pressures


def calc_rate(paths, dist_matrices, n_dict):
    rates = []
    released_pressures = []
    for path in paths:
        pressure = 0
        p_rate = 0
        time_elapsed = 0
        # print(f'1. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
        # Loop through all nodes in the path
        for idx in range(len(path) - 1):
            i = n_dict[path[idx].name]
            j = n_dict[path[idx + 1].name]
            if time_elapsed >= 30:
                break
            elif time_elapsed + dist_matrices[i][j] >= 30 and time_elapsed < 30:
                time_left = 30 - time_elapsed - 1
                pressure += p_rate * time_left
                time_elapsed = 31
                # print(f'5. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
            # If the valve has > 0 rate
            if path[idx].rate > 0:
                # print(f'On node {path[idx].name}')
                # Open it
                if time_elapsed < 30:
                    time_elapsed += 1
                    # Add its rate to the total pressure rate for the path
                    p_rate += path[idx].rate
                    # print(f'1. Sum of pressure for nodes so far: {p_rate}')
                    pressure += p_rate
                    # print(f'2. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
            if time_elapsed >= 30:
                break
            elif time_elapsed + dist_matrices[i][j] >= 30 and time_elapsed < 30:
                time_left = 30 - time_elapsed - 1
                pressure += p_rate * time_left
                time_elapsed = 31
                # print(f'5. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
            else:
                # print(f'On node {path[idx].name}. Time elapsed: {time_elapsed}. Distance: {dist_matrices[i][j]}')
                pressure += p_rate * dist_matrices[i][j]
                time_elapsed += dist_matrices[i][j]
                # print(f'3. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
                if idx == len(path) - 2:
                    if path[idx + 1].rate > 0:
                        # print(f'On node {path[idx + 1].name}')
                        # Open it
                        if time_elapsed < 30:
                            time_elapsed += 1
                            # Add its rate to the total pressure rate for the path
                            p_rate += path[idx + 1].rate
                            # print(f'1. Sum of pressure for nodes so far: {p_rate}')
                            pressure += p_rate
                            # print(f'2. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
                    if time_elapsed < 30:
                        time_left = 30 - time_elapsed - 1
                        pressure += p_rate * time_left
                        time_elapsed = 31
                        # print(f'5. Time elapsed: {time_elapsed}. Released pressure: {pressure}')
        if p_rate > -1:
            rates.append(p_rate)
            released_pressures.append(pressure)
        # print()
    return rates, released_pressures


if __name__ == '__main__':

    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    valves = parse_lines(lines)
    sorted_valves = sorted(valves, key=lambda x: x.rate, reverse=True)
    add_neighbors(lines, valves)
    for valve in valves:
        print(valve)
    dist_matrices = initialize_matrix(valves)
    print(valves)
    print(sorted_valves)
    # print(dist_matrices)
    dist_matrices = run_floyd_warshalls(valves, dist_matrices)
    print(dist_matrices)
    n_dict, i_dict = name_to_idx(valves)
    paths, sum_paths = prune_paths_2(valves, dist_matrices, n_dict)
    print(len(sum_paths))
    max_rates, rel_pressure = loop_through_prod(paths, dist_matrices, n_dict)
    print(max(rel_pressure))
    #for idx, i in enumerate(rel_pressure):
    #    if i > 1651:
    #        print(idx)
