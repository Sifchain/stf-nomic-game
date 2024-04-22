import random


def roll_dice() -> int:
    """
    Simulate rolling two six-sided dice and return the total.

    Returns:
        int: The total of the two dice rolls.
    """
    # Simulate two dice rolls
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)

    # Calculate the sum of the two rolls
    total = die1 + die2

    print(f"Rolled a {die1} and a {die2}. Total: {total}")

    return total
