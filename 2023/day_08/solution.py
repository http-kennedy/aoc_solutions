import helper as helper
import math


def parse_network(data):
    network = {}
    for line in data[1:]:
        if " = " in line:
            node, connections = line.split(" = ")
            left, right = connections.strip("()").split(", ")
            network[node] = (left, right)
        else:
            print(f"Unexpected line format: {line}")
    return network


def parse_instructions(data):
    return data[0]


@helper.profile
def solution_p1(data, debug_mode: bool = False):
    network = parse_network(data)
    instructions = parse_instructions(data)
    current_node = "AAA"
    steps = 0

    if helper.debug_solution_mode:
        print(f"Parsed Network: {network}")
        print(f"Instructions: {instructions}")

    instruction_length = len(instructions)
    i = 0

    while current_node != "ZZZ":
        direction = instructions[i % instruction_length]
        if helper.debug_solution_mode:
            print(
                f"Step {steps+1}: Current Node: {current_node}, Direction: {direction}, Next Node: {network[current_node][0 if direction == 'L' else 1]}"
            )
        current_node = network[current_node][0 if direction == "L" else 1]
        steps += 1
        i += 1

    if helper.debug_solution_mode:
        print(f"Total Steps: {steps}")
    return steps


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


@helper.profile
def solution_p2(data, debug_mode: bool = False):
    network = parse_network(data)
    instructions = parse_instructions(data)
    a_nodes = {node for node in network if node.endswith("A")}

    # precompute destinations
    destinations = {node: (network[node][0], network[node][1]) for node in network}

    # cycle lengths for each 'A' node
    cycle_lengths = []
    for a_node in a_nodes:
        steps = 0
        current_node = a_node
        while not current_node.endswith("Z"):
            direction = instructions[steps % len(instructions)]
            current_node = destinations[current_node][0 if direction == "L" else 1]
            steps += 1
        cycle_lengths.append(steps)
        if helper.debug_solution_mode:
            print(f"Cycle length for node {a_node}: {steps} steps")

    # LCM of these cycle lengths
    total_steps = math.lcm(*cycle_lengths)
    if helper.debug_solution_mode:
        print(f"Cycle lengths: {cycle_lengths}")
        print(f"LCM of cycle lengths: {total_steps}")

    return total_steps


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_example_solutions(solution_p1, solution_p2, args)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
