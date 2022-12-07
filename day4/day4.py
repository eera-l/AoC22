def task1(lines):
    count = 0
    for line in lines:
        p1, p2 = line.split(',')
        min1, max1 = p1.split('-')
        min2, max2 = p2.split('-')
        if (int(min1) <= int(min2) and int(max1) >= int(max2)) \
                or (int(min2) <= int(min1) and int(max2) >= int(max1)):
            count += 1
    print(count)


def task2(lines):
    count = 0
    for line in lines:
        p1, p2 = line.split(',')
        min1, max1 = p1.split('-')
        min2, max2 = p2.split('-')
        if (int(min1) <= int(max2) and int(max1) >= int(min2)) \
            or (int(min2) <= int(max1) and int(max2) >= int(min1)):
            count += 1
    print(count)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)