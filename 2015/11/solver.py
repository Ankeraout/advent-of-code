data = input()

def increment_password(password: str) -> str:
    pass

def is_password_valid(password: str) -> bool:
    pass

current_password = increment_password(data)

while not is_password_valid(current_password):
    increment_password(current_password)

print(current_password)
