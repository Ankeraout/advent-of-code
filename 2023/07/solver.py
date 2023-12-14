class Card:
    def __init__(self: "Card", value: int):
        self.value = value

    def __lt__(self: "Card", other: "Card") -> bool:
        return self.value < other.value
    
    def __repr__(self: "Card") -> str:
        return "123456789TJQKA"[self.value]

card_instances: dict[str, Card] = {
    "2": Card(1),
    "3": Card(2),
    "4": Card(3),
    "5": Card(4),
    "6": Card(5),
    "7": Card(6),
    "8": Card(7),
    "9": Card(8),
    "T": Card(9),
    "J": Card(10),
    "Q": Card(11),
    "K": Card(12),
    "A": Card(13),
}

class Hand:
    @staticmethod
    def get_type(hand: "Hand") -> int:
        if len(hand.card_counts) == 5:
            return 1
        
        elif len(hand.card_counts) == 4:
            return 2
        
        elif len(hand.card_counts) == 3:
            if hand.card_counts[0][1] == 3:
                return 4
            
            else:
                return 3
            
        elif len(hand.card_counts) == 2:
            if hand.card_counts[0][1] == 4:
                return 6
            
            else:
                return 5
            
        else:
            return 7
        
    @staticmethod
    def is_hand_lower(hand: list[Card], other: list[Card]) -> bool:
        if len(hand) == 0:
            return False
        
        if hand[0].value == other[0].value:
            return Hand.is_hand_lower(hand[1:], other[1:])

        else:
            return hand[0] < other[0]

    def __init__(self: "Hand", cards: list[Card], bid: int):
        self.cards = cards
        self.bid = bid

        card_set = set(card for card in cards)

        self.card_counts = sorted([(card, self.cards.count(card)) for card in card_set if self.cards.count(card) != 0], key=lambda x: x[1], reverse=True)
        self.type = Hand.get_type(self)

    def __lt__(self: "Hand", other: "Hand") -> bool:
        if self.type < other.type:
            return True

        elif self.type > other.type:
            return False
        
        else:
            return Hand.is_hand_lower(self.cards, other.cards)
        
    def __repr__(self: "Hand") -> str:
        return f"{''.join([card.__repr__() for card in self.cards])} => {self.type}"

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def parse_cards(cards_str: str) -> list[Card]:
    return [card_instances[card_str] for card_str in cards_str]

def parse_hand(hand_str: str) -> Hand:
    cards_str, bid_str = hand_str.split(" ")
    return Hand(parse_cards(cards_str), int(bid_str))

def parse_input(hands: list[str]) -> list[Hand]:
    return [parse_hand(hand_str) for hand_str in hands]

def get_answer_1(data: list[Hand]) -> int:
    return sum([(index + 1) * hand.bid for index, hand in enumerate(sorted(data))])

def main():
    data_str = read_input()
    data = parse_input(data_str)

    print(get_answer_1(data))

if __name__ == "__main__":
    main()
