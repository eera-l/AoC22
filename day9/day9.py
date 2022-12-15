import numpy as np


def is_distance_too_large(x1, x2, y1, y2):
    if np.sqrt((x1 - x2)**2 + (y1 - y2)**2) > 1.5:
        return True
    return False


def map_dir(x_h, y_h, x_t, y_t):
    # If the head has moved further horizontally than vertically
    if np.abs(x_h - x_t) > np.abs(y_h - y_t):
        if x_h < x_t:
            x_t = x_h + 1
        else:
            x_t = x_h - 1
        y_t = y_h
    elif np.abs(x_h - x_t) < np.abs(y_h - y_t):
        if y_h < y_t:
            y_t = y_h + 1
        else:
            y_t = y_h - 1
        x_t = x_h
    else:
        if x_h < x_t:
            x_t = x_h + 1
        else:
            x_t = x_h - 1
        if y_h < y_t:
            y_t = y_h + 1
        else:
            y_t = y_h - 1
    return x_t, y_t


def proceed(direction, x, y):
    if direction == 'R':
        x += 1
    elif direction == 'L':
        x -= 1
    elif direction == 'U':
        y -= 1
    elif direction == 'D':
        y += 1
    return x, y


def task1(lines):
    x_h, y_h = 500, 500
    x_t, y_t = 500, 500
    checked = np.zeros([1000, 1000], dtype=int)
    checked[y_t, x_t] = 1

    for line in lines:
        dir, steps = line.split()
        for _ in range(int(steps)):
            x_h, y_h = proceed(dir, x_h, y_h)
            if is_distance_too_large(x_h, x_t, y_h, y_t):
                x_t, y_t = map_dir(x_h, y_h, x_t, y_t)
                checked[y_t, x_t] = 1
    print(checked.flatten().sum())


def task2(lines):
    knots = 10
    xs = [500] * knots
    ys = [500] * knots
    checked = np.zeros([1000, 1000], dtype=int)
    checked[ys[-1], xs[-1]] = 1

    for line in lines:
        dir, steps = line.split()
        for _ in range(int(steps)):
            xs[0], ys[0] = proceed(dir, xs[0], ys[0])
            for i in range(1, knots):
                if is_distance_too_large(xs[i - 1], xs[i], ys[i - 1], ys[i]):
                    xs[i], ys[i] = map_dir(xs[i - 1], ys[i - 1], xs[i], ys[i])
                    if i == knots - 1:
                        checked[ys[i], xs[i]] = 1
    print(checked.flatten().sum())


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)