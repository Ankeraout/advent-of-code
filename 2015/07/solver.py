from abc import abstractmethod, ABC

import re
    
class Expression(ABC):
    @abstractmethod
    def get_value(self, wires: dict[str, int]) -> int:
        pass

    @abstractmethod
    def get_dependencies(self) -> list[str]:
        pass

class WireExpression(Expression):
    def __init__(self, variable_name: str):
        self.variable_name = variable_name
    
    def get_value(self, wires: dict[str, int]) -> int:
        return wires[self.variable_name]
    
    def get_dependencies(self) -> list[str]:
        return [self.variable_name]
    
class IntegerExpression(Expression):
    def __init__(self, value: int):
        self.value = value

    def get_value(self, wires: dict[str, int]) -> int:
        return self.value
    
    def get_dependencies(self) -> list[str]:
        return []
    
class NotExpression(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression

    def get_value(self, wires: dict[str, int]) -> int:
        return self.expression.get_value(wires) ^ 65535
    
    def get_dependencies(self) -> list[str]:
        return self.expression.get_dependencies()
    
class OrExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def get_value(self, wires: dict[str, int]) -> int:
        return self.left.get_value(wires) | self.right.get_value(wires)
    
    def get_dependencies(self) -> list[str]:
        return self.left.get_dependencies() + self.right.get_dependencies()
    
class AndExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def get_value(self, wires: dict[str, int]) -> int:
        return self.left.get_value(wires) & self.right.get_value(wires)
    
    def get_dependencies(self) -> list[str]:
        return self.left.get_dependencies() + self.right.get_dependencies()
    
class LshiftExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def get_value(self, wires: dict[str, int]) -> int:
        return (
            self.left.get_value(wires) << self.right.get_value(wires)
        ) & 65535
    
    def get_dependencies(self) -> list[str]:
        return self.left.get_dependencies() + self.right.get_dependencies()
    
class RshiftExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def get_value(self, wires: dict[str, int]) -> int:
        return (
            self.left.get_value(wires) >> self.right.get_value(wires)
        ) & 65535
    
    def get_dependencies(self) -> list[str]:
        return self.left.get_dependencies() + self.right.get_dependencies()
    
class Instruction:
    def __init__(self, expression: Expression, destination: str):
        self.expression = expression
        self.destination = destination
    
    def execute(self, wires: dict[str, int]) -> None:
        wires[self.destination] = self.expression.get_value(wires)
    
    def get_dependencies(self) -> list[str]:
        return self.expression.get_dependencies()

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

pattern_instruction = re.compile(r"^(.+) -> ([a-z]+)$")
pattern_expression_wire = re.compile(r"^([a-z]+)$")
pattern_expression_integer = re.compile(r"^(\d+)$")
pattern_expression_not = re.compile(r"^NOT (.*)$")
pattern_expression_or = re.compile(r"^(.*) OR (.*)$")
pattern_expression_and = re.compile(r"^(.*) AND (.*)$")
pattern_expression_lshift = re.compile(r"^(.*) LSHIFT (.*)$")
pattern_expression_rshift = re.compile(r"^(.*) RSHIFT (.*)$")

def parse_expression(expression: str) -> Expression:
    match = pattern_expression_wire.fullmatch(expression)

    if match:
        return WireExpression(match.group(1))
    
    match = pattern_expression_integer.fullmatch(expression)

    if match:
        return IntegerExpression(int(match.group(1)))
    
    match = pattern_expression_not.fullmatch(expression)

    if match:
        return NotExpression(parse_expression(match.group(1)))
    
    match = pattern_expression_or.fullmatch(expression)

    if match:
        return OrExpression(
            parse_expression(match.group(1)),
            parse_expression(match.group(2))
        )
    
    match = pattern_expression_and.fullmatch(expression)

    if match:
        return AndExpression(
            parse_expression(match.group(1)),
            parse_expression(match.group(2))
        )
    
    match = pattern_expression_lshift.fullmatch(expression)

    if match:
        return LshiftExpression(
            parse_expression(match.group(1)),
            parse_expression(match.group(2))
        )
    
    match = pattern_expression_rshift.fullmatch(expression)

    if match:
        return RshiftExpression(
            parse_expression(match.group(1)),
            parse_expression(match.group(2))
        )
    
    raise ValueError(f"Invalid expression: {expression}")

def parse_instruction(instruction: str) -> Instruction:
    match = pattern_instruction.fullmatch(instruction)

    if match is None:
        raise ValueError(f"Invalid instruction: {instruction}")

    return Instruction(parse_expression(match.group(1)), match.group(2))

def are_dependencies_satisfied(
    instruction: Instruction,
    wires: dict[str, int]
) -> bool:
    return all(
        dependency in wires for dependency in instruction.get_dependencies()
    )

def compute(wires: dict[str, int], instructions: list[Instruction]) -> None:
    computed: bool = True

    while computed:
        computed = False

        for instruction in instructions:
            if (
                instruction.destination not in wires
                and are_dependencies_satisfied(instruction, wires)
            ):
                instruction.execute(wires)
                computed = True

def main():
    wires = dict()
    data = read_input()
    instructions = [parse_instruction(instruction) for instruction in data]

    compute(wires, instructions)

    print(wires["a"])

    # Part 2
    wires = {
        "b": wires["a"]
    }

    compute(wires, instructions)

    print(wires["a"])

if __name__ == "__main__":
    main()
