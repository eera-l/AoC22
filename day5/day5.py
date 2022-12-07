from queue import LifoQueue


def parse_input(lines, stack_list, instr_list):
    for i in range(7, -1, -1):
        line = lines[i]
        for j in range(0, len(line), 4):
            if line[j + 1] != ' ':
                stack_list[j // 4].put(line[j + 1])

    for i in range(10, len(lines)):
        words = lines[i].split()
        instr_list.append([int(words[1]), int(words[3]), int(words[5])])
    return stack_list, instr_list


def task1(lines):
    stack_list = []
    instr_list = []
    for _ in range(9):
        stack_list.append(LifoQueue(maxsize=50))
    stack_list, instr_list = parse_input(lines, stack_list, instr_list)
    for instr in instr_list:
        for _ in range(instr[0]):
            num = stack_list[instr[1] - 1].get()
            stack_list[instr[2] - 1].put(num)
    print(''.join([stack.get() for stack in stack_list]))


def task2(lines):
    stack_list = []
    instr_list = []
    for _ in range(9):
        stack_list.append(LifoQueue(maxsize=50))
    stack_list, instr_list = parse_input(lines, stack_list, instr_list)
    for instr in instr_list:
        nums = []
        for _ in range(instr[0]):
            nums.append(stack_list[instr[1] - 1].get())
        for i in range(len(nums) - 1, -1, -1):
            stack_list[instr[2] - 1].put(nums[i])
    print(''.join([stack.get() for stack in stack_list]))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)