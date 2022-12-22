from anytree import Node
from itertools import zip_longest


class FileNode(Node):
    def __init__(self, path, parent=None):
        super(FileNode, self).__init__(path, parent)
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def extend_items(self, items):
        self.items.extend(items)


def parse_line(line):
    root = FileNode('Root')
    current = root
    skip = False
    for idx, char in enumerate(line[1:-1]):
        if skip:
            skip = False
            continue
        if char == '[':
            current = FileNode(str(idx), parent=current)
        elif char == ']':
            parent = current.parent
            parent.add_item(current.items)
            current = current.parent
        elif char != ',':
            if line[idx + 2] != ',' and line[idx + 2] != ']' and line[idx + 2] != '[':
                current.add_item(int(char + line[idx + 2]))
                skip = True
            else:
                current.add_item(int(char))
    return root


# For this, got some help from: https://github.com/sleijon1/aoc22
def check_if_right_order(first, second):
    right_order = None
    for obj1, obj2 in zip_longest(first, second):
        if obj1 is None and obj2 is not None:
            right_order = True
        elif obj1 is not None and obj2 is None:
            right_order = False
        elif isinstance(obj1, list) and isinstance(obj2, list):
            right_order = check_if_right_order(obj1, obj2)
        elif isinstance(obj1, int) and isinstance(obj2, list):
            right_order = check_if_right_order([obj1], obj2)
        elif isinstance(obj2, int) and isinstance(obj1, list):
            right_order = check_if_right_order(obj1, [obj2])
        elif isinstance(obj1, int) and isinstance(obj2, int):
            if obj1 < obj2:
                right_order = True
            elif obj1 > obj2:
                right_order = False
        if right_order is not None:
            return right_order


def task1(lines):
    checks = []
    for idx, line in enumerate(lines):
        if idx % 3 == 0:
            first_line = line
            second_line = lines[idx + 1]
            first = parse_line(first_line).items
            second = parse_line(second_line).items
            checks.append(check_if_right_order(first, second))
    print(sum([(idx + 1) for idx, num in enumerate(checks) if num]))


def task2(lines):
    lines_of_input = []
    for idx, line in enumerate(lines):
        if idx % 3 == 0:
            first_line = line
            second_line = lines[idx + 1]
            first = parse_line(first_line).items
            second = parse_line(second_line).items
            lines_of_input.append(first)
            lines_of_input.append(second)
    lines_of_input.append([[2]])
    lines_of_input.append([[6]])
    change = True
    while change:
        change = False
        for j in range(len(lines_of_input) - 1):
            if not check_if_right_order(lines_of_input[j], lines_of_input[j + 1]):
                line = lines_of_input[j]
                lines_of_input.remove(line)
                lines_of_input.append(line)
                change = True
    print((lines_of_input.index([[2]]) + 1) * (lines_of_input.index([[6]]) + 1))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)