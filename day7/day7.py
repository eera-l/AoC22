from anytree import Node, PreOrderIter, LevelOrderGroupIter

TOTAL_SIZE = 100_000
TOTAL_SPACE = 70_000_000
UNUSED_SPACE = 30_000_000


class FileNode(Node):
    def __init__(self, path, size, parent=None):
        super(FileNode, self).__init__(path, parent)
        self.size = size


def calc_size(parent):
    size = sum([node.size for node in PreOrderIter(parent)])
    return size


def task1(lines):
    root = FileNode('/', 0)
    cwd = root
    for line in lines:
        if line[:4] == '$ cd' and line[5] != '/':
            if line[5] != '.':
                cwd = FileNode(line[5:], 0, parent=cwd)
            elif line[5] == '.':
                cwd = cwd.parent
        elif line[0].isnumeric():
            cmd = line.split()
            FileNode(cmd[1], int(cmd[0]), parent=cwd)
    levels = [[{'node': node,
                'size': node.size} for node in children] for children in LevelOrderGroupIter(root)]
    sizes = []
    for level in levels:
        for node_dict in level:
            if node_dict['size'] == 0:
                sizes.append(calc_size(node_dict['node']))
    print(sum([s for s in sizes if s <= TOTAL_SIZE]))
    return sizes


def task2(sizes):
    c_unused_space = TOTAL_SPACE - sizes[0]
    desired_size = UNUSED_SPACE - c_unused_space
    print(min([s for s in sizes if s >= desired_size]))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    sizes = task1(lines)
    task2(sizes)