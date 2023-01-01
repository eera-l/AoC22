import numpy as np


def calc_manhattan_distance(x1, y1, x2, y2):
    return np.abs(x1 - x2) + np.abs(y1 - y2)


def parse_input(lines):
    sensors = []
    beacons = []
    distances = []
    for line in lines:
        a1, a2 = line.split(':')
        bs = a1.split()
        cs = a2.split()
        x_sensor = int(bs[2].split('=')[1][:-1])
        y_sensor = int(bs[3].split('=')[1])
        sensors.append((x_sensor, y_sensor))
        x_beacon = int(cs[4].split('=')[1][:-1])
        y_beacon = int(cs[5].split('=')[1])
        beacons.append((x_beacon, y_beacon))
    for idx, tup in enumerate(sensors):
        distances.append(calc_manhattan_distance(tup[0], tup[1], beacons[idx][0], beacons[idx][1]))
    return sensors, beacons, distances


def find_sensors_on_row(ranges, ROW, sensors, distances):
    o_sensors = []

    # Find sensors that overlap with the row
    for idx, range_n in enumerate(ranges):
        overlap_y = [n for n in range(max(ROW, range_n[1]), min(ROW, range_n[0]) + 1)]
        if len(overlap_y) > 0:
            o_sensors.append((sensors[idx], distances[idx]))
    return o_sensors


def find_overlaps(o_sensors, ROW, start_x_row, end_x_row):
    overlaps = []
    # Calculate range for those sensors at desired row
    for tup in o_sensors:
        diff = np.abs(tup[0][1] - ROW)
        new_range = tup[1] - diff
        overlaps.append([n for n in range(max(tup[0][0] - new_range, start_x_row), min(end_x_row,
                                                                                       tup[0][0] + new_range) + 1)])
    return overlaps


def task1(lines):
    sensors, beacons, distances = parse_input(lines)
    ranges = []

    for idx, tup in enumerate(sensors):
        ranges.append([tup[1] + distances[idx], tup[1] - distances[idx]])

    ROW = 2_000_000
    o_sensors = find_sensors_on_row(ranges, ROW, sensors, distances)
    overlaps = find_overlaps(o_sensors, ROW, -100_000_000, 100_000_000)

    unions = set.union(*map(set, overlaps))

    beaconless = set()
    for beacon in beacons:
        if beacon[1] == ROW:
            beaconless = unions.difference(set([beacon[0]]))

    print(len(beaconless) if len(beaconless) > 0 else len(unions))


def find_perimeter_points(sensors, aug_dist):
    perimeter = []
    for idx, tup in enumerate(sensors):
        range_x = [i for i in range((aug_dist[idx] - sensors[idx][0]) * -1, aug_dist[idx] + sensors[idx][0] + 1)]
        range_y = [i for i in range((aug_dist[idx] - sensors[idx][1]) * -1, aug_dist[idx] + sensors[idx][1] + 1)]
        for tup in zip(range_x[:len(range_x) // 2], range_y[len(range_y) // 2:]):
            if 0 <= tup[0] <= 4_000_000 and 0 <= tup[1] <= 4_000_000:
                perimeter.append(tup)
        for tup in zip(range_x[:len(range_x) // 2], range_y[:len(range_y) // 2][::-1]):
            if 0 <= tup[0] <= 4_000_000 and 0 <= tup[1] <= 4_000_000:
                perimeter.append(tup)
        for tup in zip(range_x[len(range_x) // 2:], range_y[len(range_y) // 2:][::-1]):
            if 0 <= tup[0] <= 4_000_000 and 0 <= tup[1] <= 4_000_000:
                perimeter.append(tup)
        for tup in zip(range_x[len(range_x) // 2:], range_y[:len(range_y) // 2]):
            if 0 <= tup[0] <= 4_000_000 and 0 <= tup[1] <= 4_000_000:
                perimeter.append(tup)
    return perimeter


def shortlist_points(perimeter, sensors, distances):
    short_listed = []
    s_dist = np.argsort(np.array(distances))
    for tup in perimeter:
        if calc_manhattan_distance(tup[0], tup[1], sensors[s_dist[-1]][0], sensors[s_dist[-1]][1]) \
                > distances[s_dist[-1]] and \
                calc_manhattan_distance(tup[0], tup[1], sensors[s_dist[-2]][0], sensors[s_dist[-2]][1]) \
                > distances[s_dist[-2]] and \
                calc_manhattan_distance(tup[0], tup[1], sensors[s_dist[-3]][0], sensors[s_dist[-3]][1]) \
                > distances[s_dist[-3]] and \
                calc_manhattan_distance(tup[0], tup[1], sensors[s_dist[-4]][0], sensors[s_dist[-4]][1]) \
                > distances[s_dist[-4]]:
            short_listed.append(tup)
    return short_listed, s_dist


def task2(lines):
    sensors, beacons, distances = parse_input(lines)
    aug_dist = [n + 1 for n in distances]
    perimeter = find_perimeter_points(sensors, aug_dist)

    short_listed, s_dist = shortlist_points(perimeter, sensors, distances)
    finals = []
    for tup in short_listed:
        if all([calc_manhattan_distance(tup[0], tup[1], sensors[dist_i][0], sensors[dist_i][1]) > distances[dist_i] \
                for dist_i in s_dist[:-4]]):
            finals.append(tup)
    for tup in finals:
        print(tup[0] * 4_000_000 + tup[1])


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.read().splitlines()
    task1(lines)
    task2(lines)