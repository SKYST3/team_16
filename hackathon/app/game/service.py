import random

def test()->int:
    sum = 0
    for i in range(100):
        sum += random.randint(1, 100)
    return sum