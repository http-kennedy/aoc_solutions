import helper as helper
import functools


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


def get_hand_type_values():
    return {
        "FIVE_OF_A_KIND": 7,
        "FOUR_OF_A_KIND": 6,
        "FULL_HOUSE": 5,
        "THREE_OF_A_KIND": 4,
        "TWO_PAIR": 3,
        "ONE_PAIR": 2,
        "HIGH_CARD": 1,
    }


def get_card_rank(card):
    values = "23456789TQKA"
    return values.index(card) if card != "J" else -1


def determine_hand_type_with_jokers(hand):
    hand_types = get_hand_type_values()
    card_counts = {card: hand.count(card) for card in set(hand)}
    if "J" in card_counts:
        joker_count = card_counts.pop("J")
        max_card = max(card_counts, key=card_counts.get, default="2")
        card_counts[max_card] = card_counts.get(max_card, 0) + joker_count

    count_freq = sorted(card_counts.values(), reverse=True)
    if count_freq[0] == 5:
        return hand_types["FIVE_OF_A_KIND"]
    if count_freq[0] == 4:
        return hand_types["FOUR_OF_A_KIND"]
    if 3 in count_freq and 2 in count_freq:
        return hand_types["FULL_HOUSE"]
    if 3 in count_freq:
        return hand_types["THREE_OF_A_KIND"]
    if count_freq.count(2) == 2:
        return hand_types["TWO_PAIR"]
    if 2 in count_freq:
        return hand_types["ONE_PAIR"]
    return hand_types["HIGH_CARD"]


def compare_hands_with_jokers(hand1, hand2):
    hand1_type = determine_hand_type_with_jokers(hand1)
    hand2_type = determine_hand_type_with_jokers(hand2)

    if hand1_type != hand2_type:
        return hand1_type - hand2_type

    for card1, card2 in zip(hand1, hand2):
        rank1 = get_card_rank(card1)
        rank2 = get_card_rank(card2)
        if rank1 != rank2:
            return rank1 - rank2
    return 0


@helper.profile
def solution_p2(data):
    hands = [line.split()[0] for line in data]
    bids = [int(line.split()[1]) for line in data]
    sorted_hands = sorted(
        zip(hands, bids),
        key=functools.cmp_to_key(
            lambda hand1, hand2: compare_hands_with_jokers(hand1[0], hand2[0])
        ),
    )

    total_winnings = sum(bid * (rank + 1) for rank, (_, bid) in enumerate(sorted_hands))

    if helper.debug_solution_mode:
        for rank, (hand, bid) in enumerate(sorted_hands):
            winning_amount = bid * (rank + 1)
            print(f"Hand: {hand}, Rank: {rank + 1}, Winning: {winning_amount}")

        print(f"Total Winnings: {total_winnings}")

    return total_winnings


if __name__ == "__main__":
    args = helper.parse_arguments()
    if args.example:
        helper.run_example_solutions(solution_p1, solution_p2, args)
    else:
        helper.run_solutions(args.input, solution_p1, solution_p2, args)
