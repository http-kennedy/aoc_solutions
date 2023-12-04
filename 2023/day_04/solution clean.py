import helper as helper


@helper.profile
def solution_p1(data, debug_mode: bool = False):
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

    total_points = 0

    for card_index, card in cards.items():
        winning_numbers, player_numbers = card
        matches = winning_numbers.intersection(player_numbers)

        if matches:
            points = 1 << (len(matches) - 1)
            total_points += points

    return total_points


@helper.profile
def solution_p2(data, debug_mode: bool = False):
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

        total_cards += count

        if match_count > 0:
            for i in range(
                card_index + 1, min(card_index + 1 + match_count, len(cards) + 1)
            ):
                card_counts[i] += count

    for card_index in range(1, len(cards) + 1):
        while card_counts[card_index] > 0:
            process_card(card_index, card_counts[card_index])
            card_counts[card_index] = 0

    return total_cards


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_example_solutions(solution_p1, solution_p2, args)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
