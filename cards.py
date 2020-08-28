import random

from Poker.pattern import get_pattern, get_boss_card

NAMES = ('3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'B', 'R')
VALUES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18)
INVALID_CARD_VALUE = 0
DECK = VALUES[:-2] * 4 + VALUES[-2:]
NAME_VALUE_DICT = dict(zip(NAMES, VALUES))
VALUE_NAME_DICT = dict(zip(VALUES, NAMES))
PASS = True
FAILED = False
SUCCEED = True


def preprocess(cards):
    if not cards:
        return []
    if isinstance(cards, str):
        char_list = list(cards.replace('10', 'T'))
        candidate_list = ['10' if char == 'T' else char for char in char_list]
    elif isinstance(cards, int):
        candidate_list = [cards]
    elif isinstance(cards, list):
        candidate_list = cards
    else:
        print("Invalid: argument illegal!", cards)
        return []
    return candidate_list


def to_values(card_list):
    return [NAME_VALUE_DICT[card] if card in NAMES else card for card in card_list]


def verify(candidate_list):
    result = PASS
    for candidate in candidate_list:
        if (candidate not in NAMES) and (candidate not in VALUES):
            print("Invalid: ", candidate, " is not a card!")
            result = FAILED
    return result


class Cards(list):
    def __init__(self, cards=[]):
        list.__init__([])
        self.add(cards)
        self.sort()

    # return a copy, in which remove all duplicate items
    def set(self):
        return Cards(list(set(self)))

    # print value list
    def print(self):
        self.sort()
        for value in self:
            print(value, end='')
        print('')

    # print name list
    def show(self, end_char='\n'):
        print(self.to_str(), end=end_char)

    def to_names(self):
        return [VALUE_NAME_DICT[value] for value in self]

    def to_str(self):
        return "".join(self.to_names())

    # will change the object
    def add(self, cards):
        candidate_list = preprocess(cards)
        if not candidate_list:
            return FAILED
        if verify(candidate_list) == FAILED:
            return FAILED
        self += to_values(candidate_list)
        return SUCCEED

    # will change the object
    def delete(self, cards):
        candidate_list = preprocess(cards)
        if not candidate_list:
            return FAILED
        value_list = to_values(candidate_list)
        for value in value_list:
            if value not in self:
                print("Invalid: card", value, " not in hand!")
                return FAILED
        for value in value_list:
            self.remove(value)
        return SUCCEED

    # will change the object
    def delete_all(self, cards):
        candidate_list = preprocess(cards)
        if not candidate_list:
            return FAILED
        value_list = to_values(candidate_list)
        for value in value_list:
            if value not in self:
                print("Invalid: card", value, " not in hand!")
                return FAILED
        for value in value_list:
            while value in self:
                self.remove(value)
        return SUCCEED

    def clone(self):
        return Cards(self)

    def contain(self, cards):
        self_clone = self.clone()
        if self_clone.delete(cards) == SUCCEED:
            return True
        else:
            return False

    # will change the object
    def shuffle(self):
        random.shuffle(self)

    def size(self):
        return len(self)

    def get_singles(self):
        single_list = Cards()
        for card in self:
            self_clone = self.clone()
            self_clone.delete_all(card)
            if self.size() - self_clone.size() == 1:
                single_list.add(card)

        single_list.sort()
        return single_list

    def get_pairs(self):
        pair_list = Cards()
        for card in self:
            self_clone = self.clone()
            self_clone.delete_all(card)
            if self.size() - self_clone.size() == 2:
                pair_list.add(card)

        pair_list.sort()
        return pair_list

    def get_triples(self):
        triple_list = Cards()
        for card in self:
            self_clone = self.clone()
            self_clone.delete_all(card)
            if self.size() - self_clone.size() == 3:
                triple_list.add(card)

        triple_list.sort()
        return triple_list

    def get_bombs(self):
        bomb_list = Cards()
        for card in self:
            self_clone = self.clone()
            self_clone.delete_all(card)
            if self.size() - self_clone.size() == 4:
                bomb_list.add(card)

        bomb_list.sort()
        return bomb_list

    def have_pattern(self):
        if get_pattern(self) is not None:
            return True
        return False

    def bigger_than(self, another_cards):
        self_pattern = get_pattern(self)
        another_pattern = get_pattern(another_cards)
        if self_pattern.bigger_than(another_pattern):
            return True

        self_boss_card = get_boss_card(self)
        another_boss_card = get_boss_card(another_cards)
        if self_pattern.equal(another_pattern) and self_boss_card > another_boss_card:
            return True

        return False


if __name__ == '__main__':
    cards = Cards('5555')
    another_cards = Cards('34567')

    cards.show()
    another_cards.show()

    print(cards.bigger_than(another_cards))
