import helper as helper


def parse_game_data(game_data):
    game_parts = game_data.split("; ")
    cube_counts = []
    for part in game_parts:
        counts = {}
        cubes = part.split(", ")
        for cube in cubes:
            number, color = cube.split(" ")
            counts[color] = int(number)
        cube_counts.append(counts)
    return cube_counts


@helper.profile
def solution_p1(data, debug_mode=False):
    available_cubes = {"red": 12, "green": 13, "blue": 14}
    possible_games = []

    for line in data:
        game_id, game_data = line.split(": ")
        game_id = int(game_id.split(" ")[1])
        cube_counts = parse_game_data(game_data)

        possible = True
        for subset in cube_counts:
            for (
                color,
                count,
            ) in subset.items():
                if count > available_cubes[color]:
                    possible = False
                    break
            if not possible:
                break

        if possible:
            possible_games.append(game_id)

    sum_of_ids = sum(possible_games)

    return sum_of_ids


def calculate_power(cubes):
    return cubes["red"] * cubes["green"] * cubes["blue"]


@helper.profile
def solution_p2(data, debug_mode=False):
    total_power = 0
    for line in data:
        game_id, game_data = line.split(": ")
        game_id = int(game_id.split(" ")[1])
        cube_counts = parse_game_data(game_data)

        min_cubes = {"red": 0, "green": 0, "blue": 0}
        for subset in cube_counts:
            for color, count in subset.items():
                min_cubes[color] = max(min_cubes[color], count)

        power = calculate_power(min_cubes)
        total_power += power

    return total_power


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_examples(solution_p1, solution_p2)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
