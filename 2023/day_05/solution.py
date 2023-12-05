import helper as helper


def parse_mappings(data):
    mappings = {}
    current_map = None

    for line in data:
        if ":" in line:
            current_map = line.split(":")[0].strip()
            mappings[current_map] = []
        elif current_map and line.strip():
            parts = line.split()
            if len(parts) == 3:
                dest_start, src_start, length = map(int, parts)
                mappings[current_map].append((src_start, dest_start, length))

    return mappings


def map_number(source, ranges):
    for src_start, dest_start, length in ranges:
        if src_start <= source < src_start + length:
            return dest_start + (source - src_start)
    return source


@helper.profile
def solution_p1(data, debug_mode: bool = False):
    """
    Finds the lowest location number that corresponds to any of the initial seed numbers.

    Args:
    data (list): Input data for the puzzle.
    debug_mode (bool): Flag to enable debugging mode.
    """
    if helper.debug_solution_mode:
        print(helper.green_text("Debugging is enabled in solution_p1"))

    mappings = parse_mappings(data)

    seeds_line = data[0]
    seeds = list(map(int, seeds_line.split(":")[1].strip().split()))
    lowest_location = float("inf")

    for seed in seeds:
        debug_output = f"Seed {seed}"
        current_number = seed
        for category in [
            "seed-to-soil map",
            "soil-to-fertilizer map",
            "fertilizer-to-water map",
            "water-to-light map",
            "light-to-temperature map",
            "temperature-to-humidity map",
            "humidity-to-location map",
        ]:
            current_number = map_number(current_number, mappings[category])
            debug_output += f", {category.split('-to-')[1]} {current_number}"

        lowest_location = min(lowest_location, current_number)

        if helper.debug_solution_mode:
            print(debug_output)

    return lowest_location


@helper.profile
def solution_p2(data, debug_mode: bool = False):
    if helper.debug_solution_mode:
        print(helper.green_text("Debugging is enabled in solution_p2"))
    return None


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_example_solutions(solution_p1, solution_p2, args)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
