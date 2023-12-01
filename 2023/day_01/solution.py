import os
import argparse
import re
from helper import (
    extract_example_data_and_answers,
    run_example,
    run_real_data,
    profile,
    infer_type,
)


def read_data(data):
    return [(line.strip()) for line in data.splitlines()]


@profile
def solution_part_a(data):
    total_sum = 0

    for line in data:
        first_digit = next((char for char in line if char.isdigit()), None)
        last_digit = next((char for char in reversed(line) if char.isdigit()), None)

        if first_digit is not None and last_digit is not None:
            two_digit_number = int(first_digit + last_digit)
            total_sum += two_digit_number

    return total_sum


def word_to_num(word) -> int:
    if word == "one":
        return 1
    elif word == "two":
        return 2
    elif word == "three":
        return 3
    elif word == "four":
        return 4
    elif word == "five":
        return 5
    elif word == "six":
        return 6
    elif word == "seven":
        return 7
    elif word == "eight":
        return 8
    elif word == "nine":
        return 9
    else:
        return int(word)


@profile
def solution_part_b(data):
    total_sum = 0

    for line in data:
        matches = re.findall(
            "(?=(one|two|three|four|five|six|seven|eight|nine|[0-9]))", line
        )
        first_digit_str = word_to_num(matches[0])
        last_digit_str = word_to_num(matches[-1])
        total_sum += int(f"{first_digit_str}{last_digit_str}")

    return total_sum


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Advent of Code solution.")
    parser.add_argument("--example", action="store_true", help="Use example data")
    args = parser.parse_args()

    if args.example:
        try:
            example_data_and_answers = extract_example_data_and_answers()
            run_example(
                example_data_and_answers, read_data, solution_part_a, solution_part_b
            )
        except Exception as e:
            print(f"Error processing example.txt:\n\n {e}\n")
            print("This format of example.txt is not currently supported.")

    else:
        run_real_data(read_data, solution_part_a, solution_part_b)
