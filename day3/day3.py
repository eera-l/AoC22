def convert_ascii(char, is_upper_case):
    if is_upper_case:
        return ord(char) - ord('A') + 27
    return ord(char) - ord('a') + 1


def task1(lines):
    score = 0
    for line in lines:
        first_comp = line[:len(line) // 2]
        second_comp = line[len(line) // 2:]
        inter = ''.join(list(set(first_comp).intersection(set(second_comp))))
        if inter.isupper():
            score += convert_ascii(inter, True)
        else:
            score += convert_ascii(inter, False)
    print(score)


def task2(lines):
    score = 0
    for i in range(0, len(lines), 3):
        inter = ''.join(list(set(lines[i]) \
                             .intersection(set(lines[i + 1])).intersection(set(lines[i + 2]))))
        if inter.isupper():
            score += convert_ascii(inter, True)
        else:
            score += convert_ascii(inter, False)
    print(score)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)