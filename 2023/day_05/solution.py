import helper as helper


def parse_mappings(data):
    mappings = {}
    current_map = None

    for line in data:
        if ":" in line:
            # new mappign category
            current_map = line.split(":")[0].strip()
            mappings[current_map] = []
        elif current_map and line.strip():
            # parse individual mapping entries with current category
            parts = line.split()
            if len(parts) == 3:
                dest_start, src_start, length = map(int, parts)
                mappings[current_map].append((src_start, dest_start, length))

    return mappings


def map_number(source, ranges):
    # map a number from source through the give ranges
    # finds appropriate mapping range that includes the source number
    # and calculates the destination number based on the mapping
    for src_start, dest_start, length in ranges:
        if src_start <= source < src_start + length:
            return dest_start + (source - src_start)
    return source


@helper.profile
def solution_p1(data, debug_mode: bool = False):
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
            # map the number through each category
            current_number = map_number(current_number, mappings[category])
            debug_output += f", {category.split('-to-')[1]} {current_number}"

        lowest_location = min(lowest_location, current_number)

        if helper.debug_solution_mode:
            print(debug_output)

    return lowest_location


def parse_seed_ranges(line):
    # split the line to extract the seed ranges and convert them to integer tuples
    parts = line.split(":")[1].strip().split()
    return [(int(parts[i]), int(parts[i + 1])) for i in range(0, len(parts), 2)]
    # each tuple is a range with a start and a length


def find_overlap(source_range, map_range):
    src_start, src_length = source_range
    map_start, map_dest, map_length = map_range

    src_end = src_start + src_length
    map_end = map_start + map_length

    # check if there is no overlap between the ranges
    if src_end <= map_start or map_end <= src_start:
        return None

    overlap_start = max(src_start, map_start)
    overlap_end = min(src_end, map_end)
    return overlap_start, overlap_end - overlap_start


def subtract_overlap(source_range, overlap_range):
    src_start, src_length = source_range
    overlap_start, overlap_length = overlap_range

    src_end = src_start + src_length
    overlap_end = overlap_start + overlap_length

    remaining_ranges = []

    # before the overlap
    if src_start < overlap_start:
        remaining_ranges.append((src_start, overlap_start - src_start))

    # after the overlap
    if overlap_end < src_end:
        remaining_ranges.append((overlap_end, src_end - overlap_end))

    return remaining_ranges


def apply_map_to_range(source_range, map_entry):
    src_start, src_length = source_range
    map_start, map_dest, map_length = map_entry

    # calculate the destination start based on the mapping entry
    dest_start = map_dest + (src_start - map_start)
    return dest_start, src_length


@helper.profile
def solution_p2(data, debug_mode: bool = False):
    if helper.debug_solution_mode:
        print(helper.green_text("Debugging is enabled in solution_p2"))

    mappings = parse_mappings(data)
    seed_ranges = parse_seed_ranges(data[0])
    lowest_location = float("inf")

    for map_category in [
        "seed-to-soil map",
        "soil-to-fertilizer map",
        "fertilizer-to-water map",
        "water-to-light map",
        "light-to-temperature map",
        "temperature-to-humidity map",
        "humidity-to-location map",
    ]:
        if helper.debug_solution_mode:
            print(f"Processing category: {helper.green_text(map_category)}")

        new_seed_ranges = []

        for seed_range in seed_ranges:
            if helper.debug_solution_mode:
                print(f"  Processing seed range: {helper.green_text(str(seed_range))}")

            to_process = [seed_range]

            # process each sub-range within the seed range
            while to_process:
                current_range = to_process.pop()

                # check overlap with each mapping entry
                for map_entry in mappings[map_category]:
                    overlap = find_overlap(current_range, map_entry)

                    if overlap:
                        # translate the overlapping range and store it
                        translated_range = apply_map_to_range(overlap, map_entry)
                        new_seed_ranges.append(translated_range)

                        # subtract the overlapping part and process the remaining parts
                        remaining_parts = subtract_overlap(current_range, overlap)
                        to_process.extend(remaining_parts)

                        if helper.debug_solution_mode:
                            print(
                                f"    Overlap found with {helper.green_text(str(map_entry))},"
                            )
                            print(
                                f"    translated to {helper.green_text(str(translated_range))}"
                            )
                            if remaining_parts:
                                print(
                                    f"    Remaining parts to process: {helper.green_text(str(remaining_parts))}"
                                )
                            else:
                                print("    No remaining parts to process.")

                        break  # move to next sub-range after processing overlap
                else:
                    # keep the range as is if no overlap was found
                    new_seed_ranges.append(current_range)
                    if helper.debug_solution_mode:
                        print(
                            f"    No overlap found, keeping range: {helper.green_text(str(current_range))}"
                        )

            if helper.debug_solution_mode:
                print(f"  Completed processing for {map_category}, new seed ranges:")
                for range in new_seed_ranges:
                    print(f"    {helper.green_text(str(range))}")

        # update seed ranges for the next mapping category
        seed_ranges = new_seed_ranges

    lowest_location = min(start for start, _ in seed_ranges)

    return lowest_location


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_example_solutions(solution_p1, solution_p2, args)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
