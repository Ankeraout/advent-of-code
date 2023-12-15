from abc import ABC, abstractmethod

class Box:
    def __init__(self: "Box", number: int) -> None:
        self.multiplier = number + 1
        self.lenses = []
        self.lenses_data = {}

    def add_lens(self: "Box", name: str, focal_length: int) -> None:
        if name not in self.lenses:
            self.lenses.append(name)

        self.lenses_data[name] = focal_length

    def remove_lens(self: "Box", name: str) -> None:
        if name in self.lenses_data:
            self.lenses.remove(name)
            del self.lenses_data[name]

    def compute_value(self: "Box") -> int:
        return_value = 0
        
        for lens_index, lens in enumerate(self.lenses):
            return_value += self.multiplier * (lens_index + 1) * self.lenses_data[lens]

        return return_value

class Instruction(ABC):
    @abstractmethod
    def execute(self: "Instruction", boxes: list[Box]) -> None:
        pass

class InstructionAdd(Instruction):
    def __init__(self: "InstructionAdd", lens: str, focal_length: int) -> None:
        self.lens = lens
        self.focal_length = focal_length
    
    def execute(self: "InstructionAdd", boxes: list[Box]) -> None:
        box_number = compute_hash(self.lens)
        boxes[box_number].add_lens(self.lens, self.focal_length)

class InstructionRemove(Instruction):
    def __init__(self: "InstructionRemove", lens: str) -> None:
        self.lens = lens

    def execute(self: "InstructionRemove", boxes: list[Box]) -> None:
        box_number = compute_hash(self.lens)
        boxes[box_number].remove_lens(self.lens)

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def parse_input(data_str: list[str]) -> list[str]:
    return data_str[0].split(",")

def update_hash(current_value: int, character: str) -> int:
    return_value = current_value + ord(character)
    return_value *= 17
    return_value &= 255

    return return_value

def compute_hash(string: str) -> int:
    return_value = 0

    for character in string:
        return_value = update_hash(return_value, character)

    return return_value

def get_answer_1(data: list[str]) -> int:
    return sum(compute_hash(string) for string in data)

def parse_instruction(instruction: str) -> Instruction:
    if instruction.endswith("-"):
        return parse_instruction_remove(instruction)
    
    else:
        return parse_instruction_add(instruction)
    
def parse_instruction_remove(instruction: str) -> InstructionRemove:
    return InstructionRemove(instruction[:-1])

def parse_instruction_add(instruction: str) -> InstructionAdd:
    split_instruction = instruction.split("=")
    return InstructionAdd(split_instruction[0], int(split_instruction[1]))

def get_answer_2(data: list[str]) -> int:
    instructions = [parse_instruction(instruction) for instruction in data]
    boxes: list[Box] = []

    for i in range(256):
        boxes.append(Box(i))
    
    for instruction in instructions:
        instruction.execute(boxes)

    return_value = 0

    for box in boxes:
        return_value += box.compute_value()
    
    return return_value

def main():
    data_str = read_input()
    data = parse_input(data_str)
    
    print(get_answer_1(data))
    print(get_answer_2(data))

if __name__ == "__main__":
    main()
