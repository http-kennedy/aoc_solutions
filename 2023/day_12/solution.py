import helper as helper


def parse_line(line):
    parts = line.split()
    spring_states = parts[0]
    group_sizes = [int(size) for size in parts[1].split(",")] if len(parts) > 1 else []
    return spring_states, group_sizes


def generate_combinations(
    spring_states,
    group_sizes,
    index=0,
    group_index=0,
    current_group_size=0,
    current_combination=None,
    counter=[0],
):
    if current_combination is None:
        current_combination = []

    if index == len(spring_states):
        if group_index == len(group_sizes) and current_group_size == 0:
            print("".join(current_combination))
            counter[0] += 1
        return

    if spring_states[index] in "?#":
        # broken spring
        if (
            group_index < len(group_sizes)
            and current_group_size < group_sizes[group_index]
        ):
            next_group_index = group_index + (
                current_group_size + 1 == group_sizes[group_index]
            )
            next_group_size = (
                0 if next_group_index > group_index else current_group_size + 1
            )
            generate_combinations(
                spring_states,
                group_sizes,
                index + 1,
                next_group_index,
                next_group_size,
                current_combination + ["#"],
                counter,
            )

    if spring_states[index] in "?.":  # operational spring
        # new group if current group of briken springs is complete or if it's an operational spring
        if (
            group_index < len(group_sizes)
            and current_group_size == group_sizes[group_index]
        ):
            generate_combinations(
                spring_states,
                group_sizes,
                index + 1,
                group_index + 1,
                0,
                current_combination + ["."],
                counter,
            )
        elif current_group_size == 0 or group_index >= len(group_sizes):
            generate_combinations(
                spring_states,
                group_sizes,
                index + 1,
                group_index,
                0,
                current_combination + ["."],
                counter,
            )

    return counter[0]


line = "?###???????? 3,2,1"
spring_states, group_sizes = parse_line(line)
print(f"Processing line: {line}")
num_combinations = generate_combinations(spring_states, group_sizes)
print(f"Total number of different valid states: {num_combinations}")


@helper.profile
def solution_p1(data, debug_mode: bool = False):
    """
    Placeholder for the solution to Part 1 of the puzzle.

    Args:
    data (list): Input data for the puzzle.
    debug_mode (bool): Flag to enable debugging mode.
    """
    if helper.debug_solution_mode:
        print(helper.green_text("Debugging is enabled in solution_p1"))
    return None


@helper.profile
def solution_p2(data, debug_mode: bool = False):
    """
    Placeholder for the solution to Part 2 of the puzzle.

    Args:
    data (list): Input data for the puzzle.
    debug_mode (bool): Flag to enable debugging mode.
    """
    if helper.debug_solution_mode:
        print(helper.green_text("\nDebugging is enabled in solution_p2"))
    return None


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_example_solutions(solution_p1, solution_p2, args)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
