def task1(lines):
    tot_calories = []
    calories = 0
    for line in lines:
        if line != '':
            calories += int(line)
        else:
            tot_calories.append(calories)
            calories = 0
    print(max(tot_calories))


def task2(lines):
    tot_calories = []
    calories = 0
    for line in lines:
        if line != '':
            calories += int(line)
        else:
            tot_calories.append(calories)
            calories = 0
    sorted_cal = sorted(tot_calories, reverse=True)
    print(sorted_cal[0] + sorted_cal[1] + sorted_cal[2])


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)