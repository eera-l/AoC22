import numpy as np

mirror_dict = {
    0: 4,
    4: 0,
    1: 3,
    3: 1,
    2: 2
}

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
                if checked[mirror_dict[i], j] == 0:
                    checked[mirror_dict[i], j] = 1
                    visibles += 1
    # for i in range(n.shape[0]):
    #     for j in range(n.shape[1]):
    #         if np.argmax(n[i, j:n.shape[1]]) == 0 and \
    #                 len(set(n[i, j:n.shape[1]])):
    #             checked[i, j] = 1
    #             visibles += 1
    for j in range(n.shape[1]):
        for i in range(n.shape[0]):
            if np.argmax(n[i, 0:j + 1]) == j:
                if checked[j, i] == 0:
                    checked[j, i] = 1
                    visibles += 1
    rev_v = np.flip(n, axis=0)
    for j in range(rev_v.shape[1]):
        for i in range(rev_v.shape[0]):
            if np.argmax(rev_v[i, 0:j + 1]) == j:
                if checked[j, i] == 0:
                    checked[j, i] = 1
                    visibles += 1
    print(visibles)


def task2(sizes):
    pass


if __name__ == '__main__':
    with open('test_input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    # task2(lines)