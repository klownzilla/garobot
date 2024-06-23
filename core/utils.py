from random import randint as randint

def generate_unique_id(id_length) -> int:
    lower = 10**(id_length - 1)
    upper = (10**id_length) - 1
    return randint(lower, upper)