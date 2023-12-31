import helper as helper


@helper.profile
def solution_p1(data, debug_mode: bool = False):
    if helper.debug_solution_mode:
        print(helper.green_text("\nDebugging is enabled in solution_p1\n"))

    # append period to avoid going out of bounds
    grid = [line.strip() + "." for line in data]

    # check if number is adjacent to a symbol (!= period and != digit)
    def is_valid(x, y, length):
        # loop through 3x3 grid around number
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + length + 1):
                # check if index is within bounds
                if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
                    # return true if character is a symbol (!= period and != digit) AKA GEAR
                    if grid[i][j] != "." and not grid[i][j].isdigit():
                        return True
        # no symbol found
        return False

    total_sum = 0
    # iterate through each row in the grid
    for i in range(len(grid)):
        current_number = ""
        # iterate through each character in the row
        for j in range(len(grid[i])):
            # if character == digit -> add to current number
            if grid[i][j].isdigit():
                current_number += grid[i][j]
            # if current_number != digit and have a current_number
            if current_number and not grid[i][j].isdigit():
                # see if number is adjacent to a symbol
                valid = is_valid(i, j - len(current_number), len(current_number))
                if valid:
                    total_sum += int(current_number)
                    if helper.debug_solution_mode:
                        print(
                            f"  Valid number {helper.green_text(current_number)} found at ({helper.green_text(str(i))}, {helper.green_text(str(j - len(current_number)))})"
                        )
                current_number = ""

    return total_sum


@helper.profile
def solution_p2(data, debug_mode: bool = False):
    if helper.debug_solution_mode:
        print(helper.green_text("\nDebugging is enabled in solution_p2\n"))

    grid = data

    # matrix to track the number of adjacent numbers for each gear
    numbers_adjacent_to_gears = [
        [0 for _ in range(len(grid[0]))] for _ in range(len(grid))
    ]

    # matrix to track the product of adjacent numbers for each gear
    gear_factors = [[1 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    def analyze_number(row, col, length, number):
        # iterate over a 3x3 grid area around the end of the number
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + length + 1):
                # skip if out of bounds
                if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
                    continue
                # if gear is found adjacent to number
                if grid[i][j] == "*":
                    # increase count of adjacent numbers and multiply factor for that gear
                    numbers_adjacent_to_gears[i][j] += 1
                    gear_factors[i][j] *= number
                    if helper.debug_solution_mode:
                        print(
                            f"  Gear at ({helper.green_text(str(i))}, {helper.green_text(str(j))}) "
                            f"adjacent to number {helper.green_text(str(number))}, "
                            f"factor updated to {helper.green_text(str(gear_factors[i][j]))}"
                        )

    # iterate over each row and column in grid
    for row in range(len(grid)):
        current_number = ""
        # iterate over each cell AND ONE EXTRA BECAUSE LAST NUMBER IN ROW
        for col in range(len(grid[row]) + 1):
            char = grid[row][col] if col < len(grid[row]) else None
            # add the digit to the current number == digit
            if char and char.isdigit():
                current_number += char
            # when current number ends (!= digit || OOB) -> analyze
            elif current_number:
                number = int(current_number)
                analyze_number(
                    row, col - len(current_number), len(current_number), number
                )
                current_number = ""

    # calculate gear ratio by summing factors of gears with 2 adjacent numbers
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
