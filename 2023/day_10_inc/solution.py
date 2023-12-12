import helper as helper


def is_valid_pipe_connection(x, y, nx, ny, grid):
    current = grid[x][y]
    neighbor = grid[nx][ny]
    dx, dy = nx - x, ny - y

    # Direction from current to neighbor
    if dx == 1:  # South
        return neighbor in "|7JSLF"
    if dx == -1:  # North
        return neighbor in "|LJ7FS"
    if dy == 1:  # East
        return neighbor in "-LJFS"
    if dy == -1:  # West
        return neighbor in "-7FJS"

    return False


def get_neighbors(x, y, grid, debug_mode):
    pipe = grid[x][y]
    directions = {
        "|": [(1, 0), (-1, 0)],  # vertical
        "-": [(0, 1), (0, -1)],  # horizontal
        "L": [(1, 0), (0, 1)],  # south and east
        "J": [(-1, 0), (0, 1)],  # north and east
        "7": [(-1, 0), (0, -1)],  # north and west
        "F": [(1, 0), (0, -1)],  # south and west
        "S": [(1, 0), (-1, 0), (0, 1), (0, -1)],  # can connect in any direction
    }

    neighbors = []
    for dx, dy in directions[pipe]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            neighbor = grid[nx][ny]
            if neighbor != ".":
                # Verify if the neighbor is valid based on the direction
                if is_valid_pipe_connection(x, y, nx, ny, grid):
                    neighbors.append((nx, ny))

    if debug_mode:
        print(f"Pipe at ({x}, {y}) [{pipe}]: neighbors -> {neighbors}")
    return neighbors


@helper.profile
def solution_p1(data, debug_mode: bool = False):
    if helper.debug_solution_mode:
        print(helper.green_text("Debugging is enabled in solution_p1"))
        print("Initial grid:")
        print("\n".join("".join(row) for row in data))

    grid = [list(line) for line in data]
    start = None

    # Find the starting position 'S'
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "S":
                start = (i, j)
                break
        if start:
            break

    if not start:
        return "No starting position found"

    visited = set()
    queue = [(start, 0)]  # (position, distance)
    max_distance = 0
    distance_grid = [["." for _ in row] for row in grid]  # To track distances

    while queue:
        (x, y), dist = queue.pop(0)
        if (x, y) in visited:
            if helper.debug_solution_mode:
                print(f"Skipping visited position: {x, y}")
            continue

        visited.add((x, y))
        distance_grid[x][y] = str(dist)  # Mark the distance
        neighbors = get_neighbors(x, y, grid, helper.debug_solution_mode)

        if helper.debug_solution_mode:
            print(f"At position ({x}, {y}), distance: {dist}, neighbors: {neighbors}")
            print("Current distance grid:")
            print("\n".join("".join(row) for row in distance_grid))

        for nx, ny in neighbors:
            if (nx, ny) not in visited:
                queue.append(((nx, ny), dist + 1))
                max_distance = max(max_distance, dist + 1)

    if helper.debug_solution_mode:
        print("Final distance grid:")
        print("\n".join("".join(row) for row in distance_grid))

    return max_distance


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
