from Poker.cards import Cards, VALUES
from Poker.matrix import multi_process_get_best_combos, Matrix
from Poker.pattern import get_pattern


def get_some_singles(combo, amount):
    singles = []
    for cards in combo:
        if get_pattern(Cards(cards)).equal(get_pattern(Cards('3'))):
            singles += cards
    if len(singles) < amount:
        return []
    else:
        return singles[:amount]


def get_some_pairs(combo, amount):
    amount = int(amount)
    pairs = []
    for cards in combo:
        if get_pattern(cards).equal(get_pattern(Cards('33'))):
            pairs += cards
    if len(pairs) / 2 < amount:
        return []
    else:
        return pairs[:amount * 2]


def get_some_accessories(combo, amount):
    singles = []
    pairs = []
    for cards in combo:
        if get_pattern(cards).equal(get_pattern(Cards('33'))):
            pairs += cards
    for cards in combo:
        if get_pattern(cards).equal(get_pattern(Cards('3'))):
            singles += cards

    if len(singles) < amount and len(pairs) / 2 < amount:
        return []
    elif len(singles) < amount <= len(pairs) / 2:
        return pairs[0:amount * 2]
    elif len(pairs) / 2 < amount <= len(singles):
        return singles[0:amount]
    else:
        if singles[amount - 1] < pairs[amount * 2 - 1]:
            return singles[:amount]
        else:
            return pairs[:amount * 2]


def ai_play(cards_inhand):
    combos = multi_process_get_best_combos(cards_inhand)

    gap_list = []
    for combo in combos:
        head_cards = combo[0]
        gap = 0
        for cards in combo:
            if (get_pattern(cards).equal(get_pattern(head_cards))) and (
                    (cards[0] - head_cards[0]) > gap):
                gap = cards[0] - head_cards[0]

        gap_list.append(gap)

    combo_list = []
    for i in range(len(gap_list)):
        if gap_list[i] == max(gap_list):
            combo_list.append(combos[i])

    best_play = []
    for combo in combo_list:
        if len(combo[0]) > len(best_play):
            best_play = combo[0]
            best_combo = combo

    # can't play bomb as a not follow cards, unless that's only choice
    if get_pattern(best_play).equal(get_pattern(Cards('3333'))):
        cards_inhand_copy = cards_inhand.clone()
        cards_inhand_copy.delete(best_play)
        return ai_play(cards_inhand_copy)

    # add pair or single if best play is a triple or triple straight
    best_combo.remove(best_play)
    if get_pattern(best_play).equal(get_pattern(Cards('333'))):
        best_play += get_some_accessories(best_combo, 1)
    elif get_pattern(best_play).equal(get_pattern(Cards('333444'))):
        best_play += get_some_accessories(best_combo, 2)
    elif get_pattern(best_play).equal(get_pattern(Cards('333444555'))):
        best_play += get_some_accessories(best_combo, 3)
    elif get_pattern(best_play).equal(get_pattern(Cards('333444555666'))):
        best_play += get_some_accessories(best_combo, 4)
    elif get_pattern(best_play).equal(get_pattern(Cards('333444555666777'))):
        best_play += get_some_accessories(best_combo, 5)

    return best_play


def ai_follow(cards_inhand, cards_to_follow):
    follow_cards = Cards()
    cards_to_follow_copy = cards_to_follow.clone()
    best_combos = multi_process_get_best_combos(cards_inhand)
    best_combos_size = len(best_combos[0])

    singles_to_follow = cards_to_follow.get_singles()
    pairs_to_follow = cards_to_follow.get_pairs()
    triples_to_follow = cards_to_follow.get_triples()

    # triples + accessories
    accessories_to_follow = Cards()
    if triples_to_follow.size() > 0 and (singles_to_follow.size() + pairs_to_follow.size()) > 0:
        cards_to_follow_copy = triples_to_follow
        if singles_to_follow.size() > 0:
            accessories_to_follow.add(singles_to_follow)
        if pairs_to_follow.size() > 0:
            accessories_to_follow.add(pairs_to_follow)

    cards_to_follow_start_card = cards_to_follow_copy[0]
    break_all = 0
    for combo in best_combos:
        if break_all == 1:
            break
        for cards in combo:
            if get_pattern(cards).equal(get_pattern(cards_to_follow_copy)) and cards[0] > cards_to_follow_start_card:
                follow_cards.add(cards)
                break_all = 1
                break

    if break_all == 0:
        cards_inhand_matrix = Matrix(cards_inhand)
        for card in VALUES:
            if break_all == 1:
                break
            if card <= cards_to_follow_start_card or card not in cards_inhand:
                continue
            for i in range(100):
                random_cards = cards_inhand_matrix.match_random(card)
                if random_cards is not None and get_pattern(random_cards).equal(get_pattern(cards_to_follow_copy)):
                    cards_inhand_copy = cards_inhand.clone()
                    cards_inhand_copy.delete(random_cards)
                    best_combos_after_follow = multi_process_get_best_combos(cards_inhand_copy)
                    best_combos_after_follow_size = len(best_combos_after_follow[0])
                    if best_combos_after_follow_size - best_combos_size > 0:
                        continue
                    else:
                        follow_cards.add(random_cards)
                        break_all = 1
                        break
        if break_all == 0:
            return Cards()

    if accessories_to_follow.size() > 0:
        cards_inhand_copy = cards_inhand.clone()
        cards_inhand_copy.delete_all(follow_cards)
        best_combos_after_follow = multi_process_get_best_combos(cards_inhand_copy)

        if singles_to_follow.size() > 0:
            singles = get_some_singles(best_combos_after_follow[0], singles_to_follow.size())
            if singles == []:
                return Cards()
            else:
                follow_cards.add(singles)
        if pairs_to_follow.size() > 0:
            pairs = get_some_pairs(best_combos_after_follow[0], pairs_to_follow.size() / 2)
            if pairs == []:
                return Cards()
            else:
                follow_cards.add(pairs)

    return follow_cards


if __name__ == '__main__':
    cards = Cards('3334444555666910JQK2')
    follow = ai_follow(cards, Cards('3334'))
    follow.show()
