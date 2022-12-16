import numpy as np


def task1(lines):
    cycles = [0] * 5000
    counter = 0
    value = 1
    for line in lines:
        if line == 'noop':
            cycles[counter] = value
            counter += 1
        elif 'addx' in line:
            cmd, num = line.split()
            cycles[counter] = value
            counter += 1
            cycles[counter] = value
            counter += 1
            value += int(num)
            cycles[counter] = value
    tot_sum = sum([cycles[i - 1] * i for i in range(20, 221, 40)])
    print(tot_sum)


def task2(lines):
    cycles = [300] * 5000
    counter = 0
    value = 1
    messages = []
    for line in lines:
        if line == 'noop':
            cycles[counter] = value
            counter += 1
        elif 'addx' in line:
            cmd, num = line.split()
            cycles[counter] = value
            counter += 1
            cycles[counter] = value
            counter += 1
            value += int(num)
            cycles[counter] = value
    n = np.array([_ for _ in cycles if _ != 300]).reshape([6, 40])
    for i in range(6):
        messages.append(''.join(['#' if j - 1 <= n[i, j] <= j + 1 else '.' for j in range(40)]))
    for message in messages:
        print(message)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)