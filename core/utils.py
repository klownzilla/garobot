from random import randint as randint

def generate_frequency_variation(frequency_variation: int) -> int:
    return randint(-frequency_variation, frequency_variation)

def generate_unique_id(id_length: int) -> int:
    lower = 10**(id_length - 1)
    upper = (10**id_length) - 1
    return randint(lower, upper)