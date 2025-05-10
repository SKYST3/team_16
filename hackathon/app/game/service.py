import random

def test(lst: list[int]) -> int:
    """
    This function takes a list of integers and returns the sum of the integers in the list.
    """
    sum = 0
    for i in range(100):
        sum += random.randint(1, 100)
    return sum

    return sum(lst)