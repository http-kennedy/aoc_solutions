import helper as helper


def generate_difference_sequence(values):
    # find difference between each pair of values in the sequence
    return [values[i + 1] - values[i] for i in range(len(values) - 1)]


def extrapolate_next_value(sequence):
    sequences = [sequence]

    if helper.debug_solution_mode:
        print(helper.green_text("Original sequence:") + f" {sequence}")

    # make sequences until all values are zero
    while sequences[-1].count(0) != len(sequences[-1]):
        next_seq = generate_difference_sequence(sequences[-1])
        sequences.append(next_seq)

        if helper.debug_solution_mode:
            print(helper.yellow_text("Generated sequence:") + f" {next_seq}")

    # start at the second to last sequence and work backwards to the first to calculate the next value
    for i in range(len(sequences) - 2, -1, -1):
        next_value = sequences[i][-1] + sequences[i + 1][-1]
        sequences[i].append(next_value)

        if helper.debug_solution_mode:
            left_value = sequences[i][-2]
            below_value = sequences[i + 1][-1]
            print(
                helper.yellow_text(
                    f"Backtracking step: {left_value} + {below_value} = {next_value}"
                )
            )

    # the next value is the last value in the first sequence
    next_value = sequences[0][-1]

    if helper.debug_solution_mode:
        print(helper.green_text("Next value:") + f" {next_value}")

        print(helper.green_text("Finalized sequence:"))
        for seq in sequences:
            print("  ".join(map(str, seq)))

        print("\n")

    return next_value


@helper.profile
def solution_p1(data, debug_mode: bool = False):
    if helper.debug_solution_mode:
        print(helper.green_text("Debugging is enabled in solution_p1\n"))

    sequences = [list(map(int, line.split())) for line in data]

    if helper.debug_solution_mode:
        print(helper.green_text(f"Parsed sequences: {sequences}\n"))

    total_sum = sum(extrapolate_next_value(sequence) for sequence in sequences)
    return total_sum


def extrapolate_previous_value(sequence):
    sequences = [sequence]

    if helper.debug_solution_mode:
        print(helper.green_text("Original sequence:") + f" {sequence}")

    # make sequences until all values are zero
    while sequences[-1].count(0) != len(sequences[-1]):
        next_seq = generate_difference_sequence(sequences[-1])
        sequences.append(next_seq)

        if helper.debug_solution_mode:
            print(helper.yellow_text("Generated sequence:") + f" {next_seq}")

    # insert a zero at the beginning of the all-zero sequence
    sequences[-1].insert(0, 0)

    # start at the second sequence and work forwards to the last to calculate the previous value
    for i in range(len(sequences) - 2, -1, -1):
        prev_value = sequences[i][0] - sequences[i + 1][0]
        sequences[i].insert(0, prev_value)

        if helper.debug_solution_mode:
            right_value = sequences[i][1]
            above_value = sequences[i + 1][0]
            print(
                helper.yellow_text(
                    f"Backtracking step: {right_value} - {above_value} = {prev_value}"
                )
            )

    prev_value = sequences[0][0]

    if helper.debug_solution_mode:
        print(helper.green_text("Previous value:") + f" {prev_value}")

        print(helper.green_text("Finalized sequence:"))
        for seq in sequences:
            print("  ".join(map(str, seq)))

        print("\n")

    return prev_value


@helper.profile
def solution_p2(data, debug_mode: bool = False):
    if helper.debug_solution_mode:
        print(helper.green_text("\nDebugging is enabled in solution_p2"))

    sequences = [list(map(int, line.split())) for line in data]

    if helper.debug_solution_mode:
        print(helper.green_text(f"Parsed sequences: {sequences}\n"))

    total_sum = sum(extrapolate_previous_value(sequence) for sequence in sequences)
    return total_sum


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_example_solutions(solution_p1, solution_p2, args)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
