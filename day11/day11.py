from queue import Queue


class Monkey:
    def __init__(self, op, test, m_t, m_f):
        self.op, self.value = op.split()
        self.test = test
        self.items = Queue()
        self.next_monkey_true = m_t
        self.next_monkey_false = m_f

    def add_item(self, item):
        self.items.put(item)

    def remove_item(self):
        return self.items.get()

    def do_calc(self, old):
        if self.value == 'old':
            num = old
        else:
            num = int(self.value)

        if self.op == '+':
            return old + num
        if self.op == '-':
            return old - num
        if self.op == '*':
            return old * num

    def do_test(self, old):
        if self.test == 'old':
            num = old
        else:
            num = int(self.test)
        if old % num == 0:
            return True
        return False


def play_round(monkeys, monkey_counter, task_one=True):
    for idx, monkey in enumerate(monkeys):
        while not monkey.items.empty():
            monkey_counter[idx] += 1
            item = monkey.remove_item()
            item = monkey.do_calc(item)
            if task_one:
                item //= 3
            else:
                item %= 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19
            if monkey.do_test(item):
                monkeys[monkey.next_monkey_true].add_item(item)
            else:
                monkeys[monkey.next_monkey_false].add_item(item)
    return monkeys, monkey_counter


def task1(lines):
    monkeys = []
    monkey_counter = [0] * 10
    for idx, line in enumerate(lines):
        if idx % 7 == 0:
            _, _, _, _, op, value = lines[idx + 2].split()
            items = lines[idx + 1].split()[2:]
            test = lines[idx + 3].split()[-1]
            m_t = lines[idx + 4].split()[-1]
            m_f = lines[idx + 5].split()[-1]
            monkey = Monkey(op=f'{op} {value}', test=test, m_t=int(m_t), m_f=int(m_f))
            for item in items:
                if item[-1] == ',':
                    item = int(item[:-1])
                else:
                    item = int(item)
                monkey.add_item(item)
            monkeys.append(monkey)
    for _ in range(20):
        monkeys, monkey_counter = play_round(monkeys, monkey_counter)
    sort_mc = sorted(monkey_counter, reverse=True)
    print(sort_mc[0] * sort_mc[1])


def task2(lines):
    monkeys = []
    monkey_counter = [0] * 10
    for idx, line in enumerate(lines):
        if idx % 7 == 0:
            _, _, _, _, op, value = lines[idx + 2].split()
            items = lines[idx + 1].split()[2:]
            test = lines[idx + 3].split()[-1]
            m_t = lines[idx + 4].split()[-1]
            m_f = lines[idx + 5].split()[-1]
            monkey = Monkey(op=f'{op} {value}', test=test, m_t=int(m_t), m_f=int(m_f))
            for item in items:
                if item[-1] == ',':
                    item = int(item[:-1])
                else:
                    item = int(item)
                monkey.add_item(item)
            monkeys.append(monkey)
    for _ in range(10_000):
        monkeys, monkey_counter = play_round(monkeys, monkey_counter, task_one=False)
    sort_mc = sorted(monkey_counter, reverse=True)
    print(sort_mc[0] * sort_mc[1])


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)