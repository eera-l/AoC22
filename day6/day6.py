def task1(lines):
    line = lines[0]
    counter = 0
    for i in range(0, len(line) - 4, 1):
        letters = line[i:i + 4]
        if len(set(letters)) == 4:
            counter += 4
            print(counter)
            break
        else:
            counter += 1


def task2(lines):
    line = lines[0]
    counter = 0
    for i in range(0, len(line) - 14, 1):
        letters = line[i:i + 14]
        if len(set(letters)) == 14:
            counter += 14
            print(counter)
            break
        else:
            counter += 1


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)