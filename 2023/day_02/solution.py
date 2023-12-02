import helper as helper


def parse_game_data(game_data):
    """
    parse the game data and return a list of dict w/ each
    having the count of cubes for each color in that subset
    """
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
    if helper.debug_solution_mode:
        print("Debugging is enabled in solution_p1")

    # available cubes for each color
    available_cubes = {"red": 12, "green": 13, "blue": 14}
    possible_games = []

    for line in data:
        # get game_id and game_data from each line
        game_id, game_data = line.split(": ")
        game_id = int(game_id.split(" ")[1])
        cube_counts = parse_game_data(game_data)

        if helper.debug_solution_mode:
            print(f"Processing Game {helper.green_text(str(game_id))}:")
            for subset in cube_counts:
                print(f"  Subset: {helper.green_text(str(subset))}")

        possible = True
        for subset in cube_counts:
            for (
                color,
                count,
            ) in subset.items():  # iterate over each color and count in the subset
                if (
                    count > available_cubes[color]
                ):  # if count is greater than available cubes for that color
                    possible = False  # nope
                    if helper.debug_solution_mode:
                        print(
                            f"    Game {helper.green_text(str(game_id))} is not possible due to {helper.red_text(str(count))} {color} cubes"
                        )
                    break
            if not possible:
                break

        # yep
        if possible:
            if helper.debug_solution_mode:
                print(f"    Game {helper.green_text(str(game_id))} is possible")
            possible_games.append(game_id)

    sum_of_ids = sum(possible_games)
    if helper.debug_solution_mode:
        print(f"Sum of IDs of possible games: {helper.green_text(str(sum_of_ids))}")

    return sum_of_ids


@helper.profile
def solution_p2(data, debug_mode=False):
    if helper.debug_solution_mode:
        print("Debugging is enabled in solution_p2")

    # find the power of a set of cubes
    def calculate_power(cubes):
        return cubes["red"] * cubes["green"] * cubes["blue"]

    total_power = 0
    for line in data:
        game_id, game_data = line.split(": ")
        game_id = int(game_id.split(" ")[1])
        cube_counts = parse_game_data(game_data)

        if helper.debug_solution_mode:
            print(f"Processing Game {helper.green_text(str(game_id))}:")
            for subset in cube_counts:
                print(f"  Subset: {helper.green_text(str(subset))}")

        # Determine the minimum set of cubes for the game
        min_cubes = {"red": 0, "green": 0, "blue": 0}
        for subset in cube_counts:
            for color, count in subset.items():
                min_cubes[color] = max(
                    min_cubes[color], count
                )  # highest count of each color in all subsets

        power = calculate_power(min_cubes)
        total_power += power

        if helper.debug_solution_mode:
            print(
                f"  Minimum cubes for Game {helper.green_text(str(game_id))}: {helper.green_text(str(min_cubes))}"
            )
            print(
                f"  Power of Game {helper.green_text(str(game_id))}: {helper.green_text(str(power))}"
            )

    if helper.debug_solution_mode:
        print(
            f"Sum of the power of minimum sets: {helper.green_text(str(total_power))}"
        )

    return total_power


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_examples(solution_p1, solution_p2)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
