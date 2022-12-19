import heapq
from queue import Queue

import numpy as np


class Cell:
    def __init__(self, parent, x, y, height):
        self.parent = parent
        self.x = x
        self.y = y
        self.height = height
        self.f, self.g, self.h = 0, 0, 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __gt__(self, other):
        return self.f > other.f

    def __ge__(self, other):
        return self.f >= other.f

    def __str__(self):
        return f'X: {self.x}, Y: {self.y}'


def heuristic(x1, x2, y1, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def find_children(cell, grid, closed_list=None):
    x = cell.x
    y = cell.y
    children = []

    for pos_x in range(x - 1, x + 2):
        for pos_y in range(y - 1, y + 2):
            if len(grid) > pos_x >= 0 and len(grid[0]) > pos_y >= 0 and \
                    (pos_x != x or pos_y != y) and (pos_x == x or pos_y == y):
                if grid[pos_x][pos_y] < cell.height or grid[pos_x][pos_y] - cell.height < 2:
                    child_cell = Cell(cell, pos_x, pos_y, grid[pos_x][pos_y])

                    if closed_list is not None:
                        result = next((i for i, v in enumerate(closed_list) \
                                       if v[1] == child_cell), None)
                        if result is None:
                            children.append(child_cell)
                    else:
                        children.append(child_cell)
    return children


def run_a_star(start_cell, end_cell, grid):
    open_list = []
    closed_list = []
    path = []

    start_cell.h = heuristic(end_cell.x, start_cell.x, end_cell.y, start_cell.y)
    start_cell.f = start_cell.g + start_cell.h

    heapq.heappush(open_list, (start_cell.f, start_cell))
    while open_list:
        current_cell = heapq.heappop(open_list)[1]
        heapq.heappush(closed_list, (current_cell.f, current_cell))

        if current_cell == end_cell:
            while current_cell.parent is not None:
                path.append(current_cell.parent)
                current_cell = current_cell.parent
            break

        children = find_children(current_cell, grid, closed_list)

        for child in children:
            if child.f < current_cell.f:
                child.g = current_cell.g + 1
                child.h = heuristic(end_cell.x, child.x, end_cell.y, child.y)
                child.f = child.g + child.h

            result = next((i for i, v in enumerate(open_list) \
                           if v[1] == child), None)
            if result is None:
                heapq.heappush(open_list, (child.f, child))
    return len(path)


def run_bfs(start_cell, end_cell, grid):
    visited = []
    bfs_queue = Queue()
    path = []

    visited.append(start_cell)
    bfs_queue.put(start_cell)

    while not bfs_queue.empty():
        current_cell = bfs_queue.get()

        if current_cell == end_cell:
            while current_cell.parent is not None:
                path.append(current_cell)
                current_cell = current_cell.parent
            break

        children = find_children(current_cell, grid)

        for child in children:
            if child not in visited:
                visited.append(child)
                bfs_queue.put(child)
    return len(path)


def task1(lines):
    grid = []
    start_cell = None
    end_cell = None
    for line in lines:
        row = [ord(char) for char in line]
        grid.append(row)
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == ord('S'):
                start_cell = Cell(None, x, y, ord('a'))
                grid[x][y] = ord('a')
            elif grid[x][y] == ord('E'):
                end_cell = Cell(None, x, y, ord('z'))
                grid[x][y] = ord('z')
    print(run_a_star(start_cell, end_cell, grid))


def task2(lines):
    grid = []
    coords = []
    start_cell = None
    end_cell = None
    paths = []
    for line in lines:
        row = [ord(char) for char in line]
        grid.append(row)
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == ord('S'):
                grid[x][y] = ord('a')
                coords.append((x, y))
            elif grid[x][y] == ord('E'):
                end_cell = Cell(None, x, y, ord('z'))
                grid[x][y] = ord('z')
            elif grid[x][y] == ord('a'):
                coords.append((x, y))
    for coord in coords:
        start_cell = Cell(None, coord[0], coord[1], ord('a'))
        paths.append(run_bfs(start_cell, end_cell, grid))
    print(sorted(paths))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)