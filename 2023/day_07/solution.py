import helper as helper


def rank_hand(hand):
    values = "AKQJT98765432"
    value_to_rank = {v: i for i, v in enumerate(values)}

    hand_ranks = [value_to_rank[card] for card in hand]

    # count frequency of each card rank
    counts = {rank: hand_ranks.count(rank) for rank in set(hand_ranks)}
    hand_type = determine_hand_type(counts)

    if helper.debug_solution_mode:
        print(f"Hand: {hand}, Hand Ranks: {hand_ranks}, Type: {hand_type}")

    return (hand_type,) + tuple(hand_ranks)


def determine_hand_type(counts):
    frequencies = sorted(counts.values(), reverse=True)
    if frequencies[0] == 5:
        return 1  # five of a kind
    elif frequencies[0] == 4:
        return 2  # four of a kind
    elif frequencies[0] == 3 and frequencies[1] == 2:
        return 3  # full house
    elif frequencies[0] == 3:
        return 4  # three of a kind
    elif frequencies[0] == 2 and frequencies[1] == 2:
        return 5  # two pair
    elif frequencies[0] == 2:
        return 6  # one pair
    else:
        return 7  # high card


@helper.profile
def solution_p1(data):
    hands = [line.split()[0] for line in data]
    bids = [int(line.split()[1]) for line in data]

    ranked_hands = [(rank_hand(hand), idx) for idx, hand in enumerate(hands)]
    # sort by hand type -> card ranks
    ranked_hands.sort(key=lambda x: x[0])

    if helper.debug_solution_mode:
        print("Ranked Hands:")
        for rank, idx in ranked_hands:
            print(f"Rank: {rank}, Hand: {hands[idx]}, Bid: {bids[idx]}")

    total_winnings = 0
    for i, (_, idx) in enumerate(ranked_hands):
        rank = len(hands) - i  # weakest hand has rank 1
        winning = bids[idx] * rank
        total_winnings += winning
        if helper.debug_solution_mode:
            print(f"Hand: {hands[idx]}, Rank: {rank}, Winning: {winning}")

    if helper.debug_solution_mode:
        print(f"Total Winnings: {total_winnings}")

    return total_winnings


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
