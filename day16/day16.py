import heapq
from collections import defaultdict

import numpy as np


class Valve:
    def __init__(self, name, rate, children):
        self.name = name
        self.children = children
        self.rate = rate
        self.f, self.g, self.h = 0, 0, 0

    def __eq__(self, other):
        return self.name == other.name


def heuristic(valve, minutes):
    return valve.rate * minutes


def find_children(valve):
    return valve.children


def run_a_star(start_valve, end_valve, valve_dict):
    open_list = []
    closed_list = []
    path = []
    minutes = 30

    start_valve.h = heuristic(end_valve, minutes - 1)
    start_valve.f = start_valve.g + start_valve.h

    heapq.heappush(open_list, (start_valve.f, start_valve))
    while open_list:
        current_valve = heapq.heappop(open_list)[1]
        heapq.heappush(closed_list, (current_valve.f, current_valve))

        if current_valve == end_valve:
            while valve_dict[current_valve] is not None:
                path.append(valve_dict[current_valve])
                current_valve = valve_dict[current_valve]
            break

        children = find_children(current_valve)

        for child in children:
            if child.f < current_valve.f:
                child.g = current_valve.g + 1
                child.h = heuristic(child, minutes - 2)
                child.f = child.g + child.h

            result = next((i for i, v in enumerate(open_list) \
                           if v[1] == child), None)
            if result is None:
                heapq.heappush(open_list, (child.f, child))
    return len(path)


def parse_lines(lines):
    valves = []
    min_valve_rate = np.inf
    min_valve_name = ''
    for line in lines:
        first, second = line.split(';')
        firsts = first.split()
        valve_name = firsts[1]
        valve_rate = int(firsts[4].split('=')[1])
        if 0 < valve_rate < min_valve_rate:
            min_valve_rate = valve_rate
            min_valve_name = valve_name
        try:
            seconds = second.split('valves ')[1].split(', ')
        except IndexError:
            seconds = second.split('valve ')[1]
        valves.append(Valve(valve_name, valve_rate, seconds))
    valve_dict = make_parent_dict(valves)
    pass


def make_parent_dict(valves):
    valve_dict = defaultdict(str)
    for valve in valves:
        for child in valve.children:
            valve_dict[child] = valve.name
    return valve_dict


def task1(lines):
    parse_lines(lines)


def task2(lines):
    pass


if __name__ == '__main__':
    with open('test_input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    # task2(lines)
