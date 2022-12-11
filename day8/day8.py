import numpy as np


def find_specular(index, length):
    return length - 1 - index


def task1(lines):
    nums = []
    for line in lines:
        nums.append([int(l) for l in line])
    n = np.array([np.array(line) for line in nums])
    checked = np.zeros_like(n)

    visibles = 0
    for i in range(n.shape[0]):
        for j in range(n.shape[1]):
            if np.argmax(n[i, 0:j + 1]) == j:
                checked[i, j] = 1
                visibles += 1
    rev_h = np.flip(n, axis=1)
    for i in range(rev_h.shape[0]):
        for j in range(rev_h.shape[1]):
            if np.argmax(rev_h[i, 0:j + 1]) == j:
                if checked[i, find_specular(j, rev_h.shape[1])] == 0:
                    checked[i, find_specular(j, rev_h.shape[1])] = 1
                    visibles += 1
    for j in range(n.shape[1]):
        for i in range(n.shape[0]):
            if np.argmax(n[0:i + 1, j]) == i:
                if checked[i, j] == 0:
                    checked[i, j] = 1
                    visibles += 1
    rev_v = np.flip(n, axis=0)
    for j in range(rev_v.shape[1]):
        for i in range(rev_v.shape[0]):
            if np.argmax(rev_v[0:i + 1, j]) == i:
                if checked[find_specular(i, rev_v.shape[0]), j] == 0:
                    checked[find_specular(i, rev_v.shape[0]), j] = 1
                    visibles += 1
    print(visibles)


def task2(lines):
    nums = []
    for line in lines:
        nums.append([int(l) for l in line])
    n = np.array([np.array(line) for line in nums])
    checked = np.zeros_like(n)

    for i in range(n.shape[0]):
        for j in range(n.shape[1]):
            if len(n[i, 0:j]) > 0:
                a = np.flip(n[i, 0:j])
                set = False
                for k in range(a.size):
                    if a[k] >= n[i, j]:
                        checked[i, j] = k + 1
                        set = True
                        break
                if not set:
                    checked[i, j] = a.size
    rev_h = np.flip(n, axis=1)
    for i in range(rev_h.shape[0]):
        for j in range(rev_h.shape[1]):
            if len(rev_h[i, 0:j]) > 0:
                a = np.flip(rev_h[i, 0:j])
                set = False
                for k in range(a.size):
                    if a[k] >= rev_h[i, j]:
                        checked[i, find_specular(j, rev_h.shape[1])] *= k + 1
                        set = True
                        break
                if not set:
                    checked[i, find_specular(j, rev_h.shape[1])] *= a.size
            else:
                checked[i, find_specular(j, rev_h.shape[1])] *= 0
    for j in range(n.shape[1]):
        for i in range(n.shape[0]):
            if len(n[0:i, j]) > 0:
                a = np.flip(n[0:i, j])
                set = False
                for k in range(a.size):
                    if a[k] >= n[i, j]:
                        checked[i, j] *= k + 1
                        set = True
                        break
                if not set:
                    checked[i, j] *= a.size
            else:
                checked[i, j] *= 0
    rev_v = np.flip(n, axis=0)
    for j in range(rev_v.shape[1]):
        for i in range(rev_v.shape[0]):
            if len(rev_v[0:i, j]) > 0:
                a = np.flip(rev_v[0:i, j])
                set = False
                for k in range(a.size):
                    if a[k] >= rev_v[i, j]:
                        checked[find_specular(i, rev_v.shape[0]), j] *= k + 1
                        set = True
                        break
                if not set:
                    checked[find_specular(i, rev_v.shape[0]), j] *= a.size
            else:
                checked[find_specular(i, rev_v.shape[0]), j] *= 0
    print(np.max(checked.flatten()))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)