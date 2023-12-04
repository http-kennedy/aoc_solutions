import helper as helper


@helper.profile
def solution_p1(data, debug_mode: bool = False):
    """
    Calculate the total points from the scratchcard data.

    Args:
    data (list): Input data for the puzzle, each element is a line.
    debug_mode (bool): Flag to enable debugging mode.
    """
    if helper.debug_solution_mode:
        print(helper.green_text("Debugging is enabled in solution_p1"))

    cards = {}

    for line in data:
        if line.strip() == "":
            continue

        card_index, numbers = line.split(":")
        winning, player = numbers.split("|")
        cards[card_index.strip()] = (
            set(map(int, winning.split())),
            set(map(int, player.split())),
        )

        if helper.debug_solution_mode:
            print(
                f"Processing {card_index.strip()}: Winning numbers [{winning}], Player's numbers [{player}]"
            )

    total_points = 0

    for card_index, card in cards.items():
        winning_numbers, player_numbers = card
        matches = winning_numbers.intersection(player_numbers)

        if helper.debug_solution_mode:
            matches_text = (
                helper.green_text(f"{matches}\n") if matches else "No matches\n"
            )
            print(
                f"Card {card_index}: Winning numbers {winning_numbers}, Player's numbers {player_numbers}, Matches: {matches_text}"
            )

        if matches:
            # 2^(number of matches - 1)
            points = 1 << (len(matches) - 1)
            total_points += points

            if helper.debug_solution_mode:
                print(
                    f"Calculating points for Card {card_index}: Matches found: {len(matches)}, Points for this card: {points}\n"
                )

    return total_points


@helper.profile
def solution_p2(data, debug_mode: bool = False):
    """
    Calculate the total number of scratchcards including the copies won.

    Args:
    data (list): Input data for the puzzle.
    debug_mode (bool): Flag to enable debugging mode.
    """
    if helper.debug_solution_mode:
        print(helper.green_text("Debugging is enabled in solution_p2"))

    cards = {}
    for line in data:
        if line.strip() == "":
            continue

        card_index, numbers = line.split(":")
        winning, player = numbers.split("|")
        cards[int(card_index.split()[1])] = (
            set(map(int, winning.split())),
            set(map(int, player.split())),
        )

    total_cards = 0
    card_counts = {i: 1 for i in cards}

    def process_card(card_index, count):
        nonlocal total_cards
        winning_numbers, player_numbers = cards[card_index]
        matches = winning_numbers.intersection(player_numbers)
        match_count = len(matches)

        # include current copies
        total_cards += count

        # scratch winning new copies
        if match_count > 0:
            for i in range(
                card_index + 1, min(card_index + 1 + match_count, len(cards) + 1)
            ):
                card_counts[i] += count
                if helper.debug_solution_mode:
                    print(
                        f"Card {card_index}: Processing {count} copies, Winning numbers {winning_numbers}, Player's numbers {player_numbers}, Matches: {helper.green_text(f'{matches}')}, Won {helper.green_text(f'{count}')} copies of card {helper.green_text(f'{i}')}"
                    )

    # scratch each card and its copies
    for card_index in range(1, len(cards) + 1):
        while card_counts[card_index] > 0:
            process_card(card_index, card_counts[card_index])
            # DONT FORGET TO RESET THE COUNT -,-
            card_counts[card_index] = 0

    if helper.debug_solution_mode:
        print(f"Total scratchcards including copies: {total_cards}")

    return total_cards


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_example_solutions(solution_p1, solution_p2, args)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
