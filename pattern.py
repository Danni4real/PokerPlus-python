INVALID_PATTERN = 0


def get_pattern(cards):
    pattern = Pattern()
    single_cards = cards.get_singles()
    pair_cards = cards.get_pairs()
    triple_cards = cards.get_triples()
    bomb_cards = cards.get_bombs()

    single_cards.sort()
    pair_cards.sort()
    triple_cards.sort()
    bomb_cards.sort()

    single_amount = single_cards.set().size()
    pair_amount = pair_cards.set().size()
    triple_amount = triple_cards.set().size()
    bomb_amount = bomb_cards.set().size()

    cards_clone = cards.clone()
    cards_clone.sort()
    if cards_clone.to_str() == 'BR':
        pattern.is_nuke = True
    elif single_amount + pair_amount + triple_amount + bomb_amount == 1:
        pass
    elif single_amount > 0 and \
            pair_amount == 0 and \
            triple_amount > 0 and \
            bomb_amount == 0 and \
            single_amount == triple_amount and \
            is_straight(triple_cards.set()):
        pass
    elif single_amount == 0 and \
            pair_amount > 0 and \
            triple_amount > 0 and \
            bomb_amount == 0 and \
            pair_amount == triple_amount and \
            is_straight(triple_cards.set()):
        pass
    elif single_amount > 4 and \
            pair_amount == 0 and \
            triple_amount == 0 and \
            bomb_amount == 0 and \
            is_straight(single_cards):
        pass
    elif single_amount == 0 and \
            pair_amount > 2 and \
            triple_amount == 0 and \
            bomb_amount == 0 and \
            is_straight(pair_cards.set()):
        pass
    elif single_amount == 0 and \
            pair_amount == 0 and \
            triple_amount > 1 and \
            bomb_amount == 0 and \
            is_straight(triple_cards.set()):
        pass
    elif single_amount == 2 and \
            pair_amount == 0 and \
            triple_amount == 0 and \
            bomb_amount == 1:
        pass
    elif single_amount == 0 and \
            pair_amount == 2 and \
            triple_amount == 0 and \
            bomb_amount == 1:
        pass
    else:
        return None

    pattern.single_amount = single_amount
    pattern.pair_amount = pair_amount
    pattern.triple_amount = triple_amount
    pattern.bomb_amount = bomb_amount

    if bomb_amount >= 1:
        pattern.boss_card = bomb_cards[-1]
    elif triple_amount >= 1:
        pattern.boss_card = triple_cards[-1]
    elif pair_amount >= 1:
        pattern.boss_card = pair_cards[-1]
    elif single_amount >= 1:
        pattern.boss_card = single_cards[-1]

    return pattern


def get_boss_card(cards):
    pattern = get_pattern(cards)
    return pattern.boss_card


def is_straight(cards):
    cards_clone = cards.clone()
    cards_clone.sort()
    for i in range(cards_clone.size()):
        if i == 0:
            continue
        if not cards_clone[i] - cards_clone[i - 1] == 1:
            return False
    return True


class Pattern:
    def __init__(self):
        self.boss_card = 0
        self.single_amount = 0
        self.pair_amount = 0
        self.triple_amount = 0
        self.bomb_amount = 0
        self.is_nuke = False

    def show(self):
        print(self.single_amount, self.pair_amount, self.triple_amount, self.bomb_amount, self.is_nuke)

    def bigger_than(self, another_pattern):
        if self.bomb_amount == 1 and another_pattern.bomb_amount == 0 and not another_pattern.is_nuke:
            return True
        if self.is_nuke:
            return True

    def equal(self, another_pattern):
        if self.single_amount == another_pattern.single_amount and \
                self.pair_amount == another_pattern.pair_amount and \
                self.triple_amount == another_pattern.triple_amount and \
                self.bomb_amount == another_pattern.bomb_amount and \
                self.is_nuke == another_pattern.is_nuke:
            return True
        return False
