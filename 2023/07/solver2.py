class Card:
    def __init__(self: "Card", value: int):
        self.value = value

    def __lt__(self: "Card", other: "Card") -> bool:
        return self.value < other.value
    
    def __repr__(self: "Card") -> str:
        return "J23456789TQKA"[self.value]

card_instances: dict[str, Card] = {
    "J": Card(0),
    "2": Card(1),
    "3": Card(2),
    "4": Card(3),
    "5": Card(4),
    "6": Card(5),
    "7": Card(6),
    "8": Card(7),
    "9": Card(8),
    "T": Card(9),
    "Q": Card(10),
    "K": Card(11),
    "A": Card(12)
}

class Hand:
    types = [
        "None",
        "High card",
        "One pair",
        "Two pair",
        "Three of a kind",
        "Full house",
        "Four of a kind",
        "Five of a kind"
    ]

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

    def __init__(self: "Hand", cards: list[Card], bid: int):
        self.cards = cards
        self.bid = bid

        card_set = set(card for card in cards)

        self.card_counts = [(card, self.cards.count(card)) for card in card_set if card.value != 0]
        self.card_counts = sorted(self.card_counts, key=lambda x: x[0], reverse=True)
        self.card_counts = sorted(self.card_counts, key=lambda x: x[1], reverse=True)

        if len(self.card_counts) == 0:
            self.card_counts = [(card_instances["A"], 5)]
        
        else:
            self.card_counts[0] = (
                self.card_counts[0][0],
                self.card_counts[0][1] + self.cards.count(card_instances["J"])
            )

        self.type = Hand.get_type(self)

    def __lt__(self: "Hand", other: "Hand") -> bool:
        if self.type < other.type:
            return True

        elif self.type > other.type:
            return False
        
        else:
            for index in range(5):
                if self.cards[index].value < other.cards[index].value:
                    return True
                
                elif other.cards[index].value < self.cards[index].value:
                    return False

            return False
        
    def __repr__(self: "Hand") -> str:
        return f"{''.join([card.__repr__() for card in self.cards])} => {Hand.types[self.type]}"

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

def get_answer_2(data: list[Hand]) -> int:
    return sum([(index + 1) * hand.bid for index, hand in enumerate(sorted(data))])

def main():
    data_str = read_input()
    data = parse_input(data_str)
    print(get_answer_2(data))

if __name__ == "__main__":
    main()
