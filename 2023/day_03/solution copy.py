import helper as helper


@helper.profile
def solution_p1(data, debug_mode: bool = False):
    if helper.debug_solution_mode:
        print(helper.green_text("\nDebugging is enabled in solution_p1\n"))

    grid = [line.strip() + "." for line in data]

    def is_valid(x, y, length):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + length + 1):
                if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
                    if grid[i][j] != "." and not grid[i][j].isdigit():
                        return True
        return False

    total_sum = 0

    for i in range(len(grid)):
        current_number = ""
        for j in range(len(grid[i])):
            if grid[i][j].isdigit():
                current_number += grid[i][j]
            if current_number and not grid[i][j].isdigit():
                valid = is_valid(i, j - len(current_number), len(current_number))
                if valid:
                    total_sum += int(current_number)
                current_number = ""

    return total_sum


@helper.profile
def solution_p2(data, debug_mode: bool = False):
    if helper.debug_solution_mode:
        print(helper.green_text("\nDebugging is enabled in solution_p2\n"))

    grid = data

    numbers_adjacent_to_gears = [
        [0 for _ in range(len(grid[0]))] for _ in range(len(grid))
    ]

    gear_factors = [[1 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    def analyze_number(row, col, length, number):
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + length + 1):
                if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
                    continue
                if grid[i][j] == "*":
                    numbers_adjacent_to_gears[i][j] += 1
                    gear_factors[i][j] *= number

    for row in range(len(grid)):
        current_number = ""
        for col in range(len(grid[row]) + 1):
            char = grid[row][col] if col < len(grid[row]) else None
            if char and char.isdigit():
                current_number += char
            elif current_number:
                number = int(current_number)
                analyze_number(
                    row, col - len(current_number), len(current_number), number
                )
                current_number = ""

    total_gear_ratio = sum(
        gear_factors[i][j]
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if numbers_adjacent_to_gears[i][j] == 2
    )

    return total_gear_ratio


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_example_solutions(solution_p1, solution_p2, args)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
