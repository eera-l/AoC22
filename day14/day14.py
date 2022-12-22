import numpy as np


def create_grid(lines):
    grid = np.zeros(shape=(1000, 1000), dtype=int)
    # Sand source
    grid[0, 500] = 1
    max_x = 0
    for line in lines:
        coords = line.split(' -> ')
        for i in range(len(coords) - 1):
            y1, x1 = coords[i].split(',')
            y2, x2 = coords[i + 1].split(',')
            if int(x1) > max_x:
                max_x = int(x1)
            if int(x2) > max_x:
                max_x = int(x2)
            if int(x1) == int(x2):
                l = np.full(shape=[1, np.abs(int(y1) - int(y2)) + 1], fill_value=4)
                start = min(int(y1), int(y2))
                end = max(int(y1), int(y2))
                grid[int(x1), start:end + 1] = l
            elif int(y1) == int(y2):
                l = np.full(shape=[np.abs(int(x1) - int(x2)) + 1, ], fill_value=4)
                start = min(int(x1), int(x2))
                end = max(int(x1), int(x2))
                grid[start:end + 1, int(y1)] = l
    return grid, max_x


def do_step(grid, x_coord, y_coord):
    stopped = False
    if grid[x_coord, y_coord] == 4 or grid[x_coord, y_coord] == 3:
        if grid[x_coord, y_coord - 1] == 4 or grid[x_coord, y_coord - 1] == 3:
            if grid[x_coord, y_coord + 1] == 4 or grid[x_coord, y_coord + 1] == 3:
                stopped = True
            else:
                y_coord += 1
                grid[x_coord, y_coord] = 3
        else:
            y_coord -= 1
            grid[x_coord, y_coord] = 3
    else:
        grid[x_coord, y_coord] = 3
    return grid, stopped, y_coord


def fall_sand(grid, infinite, counter_stopped):
    stopped = False
    counter = 0
    y = 500
    while not stopped:
        tmp_y = y
        grid, stopped, y = do_step(grid, counter, y)
        if not stopped:
            if tmp_y == y and grid[counter - 1, y] != 4 and grid[counter - 1, y] != 1:
                grid[counter - 1, y] = 0
            elif tmp_y < y and grid[counter - 1, y - 1] != 4 and grid[counter - 1, y - 1] != 1:
                grid[counter - 1, y - 1] = 0
            elif tmp_y > y and grid[counter - 1, y + 1] != 4 and grid[counter - 1, y + 1] != 1:
                grid[counter - 1, y + 1] = 0
        else:
            counter_stopped += 1
            if counter == 1 and y == 500:
                infinite = True
        counter += 1
        if y >= grid.shape[1] or counter >= grid.shape[0]:
            infinite = True
            stopped = True
    return infinite, grid, counter_stopped


def task1(lines):
    grid, lower_bound_x = create_grid(lines)
    infinite = False
    counter_stopped = 0
    while not infinite:
        infinite, grid, counter_stopped = fall_sand(grid, infinite, counter_stopped)
    print(counter_stopped)


def task2(lines):
    grid, lower_bound_x = create_grid(lines)
    grid[lower_bound_x + 2, 0:1000] = np.full(shape=[1, 1000], fill_value=4)
    infinite = False
    counter_stopped = 0
    while not infinite:
        infinite, grid, counter_stopped = fall_sand(grid, infinite, counter_stopped)
    print(counter_stopped)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)