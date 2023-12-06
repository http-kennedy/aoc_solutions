import helper as helper


def parse_input(data):
    time_values, distance_values = [
        list(map(int, line.split(":")[1].strip().split())) for line in data
    ]

    return time_values, distance_values


@helper.profile
def solution_p1(data, debug_mode=False):
    time_values, distance_values = parse_input(data)
    result = 1

    for race_time, record_distance in zip(time_values, distance_values):
        winning_ways = 0
        for hold_time in range(race_time):
            if hold_time * (race_time - hold_time) > record_distance:
                winning_ways += 1

        result *= winning_ways

    return result


def parse_input_part2(data):
    time_value = int("".join(data[0].split(":")[1].split()))
    distance_value = int("".join(data[1].split(":")[1].split()))

    return time_value, distance_value


@helper.profile
def solution_p2(data, debug_mode=False):
    race_time, record_distance = parse_input_part2(data)
    winning_ways = 0

    for hold_time in range(race_time):
        if hold_time * (race_time - hold_time) > record_distance:
            winning_ways += 1

    return winning_ways


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_example_solutions(solution_p1, solution_p2, args)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
