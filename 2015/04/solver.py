import hashlib

data = input()

def find(data: str, nb_zeros: int) -> int:
    number = 0
    zeros_string = "0" * nb_zeros

    while not hashlib.md5(bytes(data + str(number), encoding="utf-8")).digest().hex().startswith(zeros_string):
        number += 1

    return number

print(find(data, 5))
print(find(data, 6))
