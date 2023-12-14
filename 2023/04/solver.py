from dataclasses import dataclass
import re

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

@dataclass
class Card:
    number: int
    winning: list[int]
    mine: list[int]

pattern_card = re.compile(r"^Card +(\d+): ([^|]+)\| (.*)$")

def parse_list(list: str) -> list[int]:
    return [int(x) for x in list.split(" ") if len(x) > 0]

def parse_input(data: list[str]) -> list[Card]:
    card_list = []

    for card_str in data:
        card_match = pattern_card.fullmatch(card_str)

        if card_match is None:
            raise ValueError()
        
        card_number = int(card_match.group(1))
        card_winning = parse_list(card_match.group(2))
        card_mine = parse_list(card_match.group(3))
        card_list.append(Card(card_number, card_winning, card_mine))

    return card_list

def get_card_wins(card: Card) -> int:
    count = 0

    for number in card.mine:
        if number in card.winning:
            count += 1

    return count

def get_card_points(card: Card) -> int:
    count = get_card_wins(card)
    return 2 ** (count - 1) if count != 0 else 0

def get_new_cards(cards: list[Card]) -> list[Card]:
    return cards[1:1 + get_card_wins(cards[0])]

def main():
    data = read_input()
    parsed_input = parse_input(data)
    print(sum(get_card_points(card) for card in parsed_input))

    new_cards = parsed_input.copy()

    index = 0

    while index < len(new_cards):
        wins = get_new_cards(parsed_input[new_cards[index].number - 1:])
        new_cards += wins
        index += 1

    print(len(new_cards))

if __name__ == "__main__":
    main()
