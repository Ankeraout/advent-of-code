import json

def read_input() -> str:
    return input()

def parse_input(data_str: str) -> list | dict | int | str:
    return json.loads(data_str)

def get_answer_1(data: list | dict | int | str) -> int:
    if type(data) is list:
        return sum(get_answer_1(element) for element in data)
    
    elif type(data) is dict:
        return sum(get_answer_1(element) for element in data.values())
    
    elif type(data) is int:
        return data
    
    else:
        return 0
    
def get_answer_2(data: list | dict | int | str) -> int:
    if type(data) is list:
        return sum(get_answer_2(element) for element in data)
    
    elif type(data) is dict:
        if "red" in data.values():
            return 0
        
        else:
            return sum(get_answer_2(element) for element in data.values())
    
    elif type(data) is int:
        return data
    
    else:
        return 0

def main() -> None:
    data_str = read_input()
    data = parse_input(data_str)

    print(get_answer_1(data))
    print(get_answer_2(data))

if __name__ == "__main__":
    main()
