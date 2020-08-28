import _thread
import profile
import random
import operator
import sys
import time
import multiprocessing

from Poker.cards import Cards, VALUES

MATRIX_WIDTH = VALUES[-1] + 1
MATRIX_HEIGHT = 4


def remove_dup_combo(combo_list):
    final_combos = []

    for i in range(len(combo_list)):
        for n in range(len(combo_list)):
            if n <= i:
                continue
            if combo_list[i] is not None:
                combo_list[i].sort()
            if combo_list[n] is not None:
                combo_list[n].sort()
            if operator.eq(combo_list[i], combo_list[n]):
                combo_list[n] = None

    for combo in combo_list:
        if combo is not None:
            final_combos.append(combo)

    return final_combos


class Matrix:
    def __init__(self, cards):
        self.matrix = []
        for i in range(MATRIX_WIDTH):
            self.matrix.append([0] * MATRIX_HEIGHT)
        self.match_func_list = [self.match_1x1, self.match_1x2, self.match_1x3, self.match_1x4, self.match_5x1,
                                self.match_6x1, self.match_7x1, self.match_8x1, self.match_9x1, self.match_10x1,
                                self.match_11x1, self.match_12x1, self.match_3x2, self.match_4x2, self.match_5x2,
                                self.match_6x2, self.match_7x2, self.match_8x2, self.match_9x2, self.match_10x2,
                                self.match_2x3, self.match_3x3, self.match_4x3, self.match_5x3, self.match_6x3
                                ]
        self.current_best_combo_length = 100

        for card in cards:
            if self.matrix[card][0] == 0:
                self.matrix[card][0] = 1
            elif self.matrix[card][1] == 0:
                self.matrix[card][1] = 1
            elif self.matrix[card][2] == 0:
                self.matrix[card][2] = 1
            elif self.matrix[card][3] == 0:
                self.matrix[card][3] = 1

    def show(self):
        print('  3 4 5 6 7 8 9 10J Q K A   2   B   R')
        for h in range(MATRIX_HEIGHT):
            for w in range(MATRIX_WIDTH):
                if self.matrix[w][h] == 1:
                    print(self.matrix[w][h], end=' ')
                else:
                    print(' ', end=' ')
            print('')

    def to_cards(self):
        cards = Cards()
        for h in range(MATRIX_HEIGHT):
            for w in range(MATRIX_WIDTH):
                if self.matrix[w][h] == 1:
                    cards.append(w)
        return cards

    # not change object
    def delete(self, cards):
        self_cards = self.to_cards()
        self_cards.delete(cards)
        return Matrix(self_cards)

    def match(self, start_card, another_matrix):
        width = len(another_matrix)
        height = len(another_matrix[0])
        result = 1
        match_cards = []
        for w in range(width):
            for h in range(height):
                if start_card + w <= VALUES[-1]:
                    result *= another_matrix[w][h]
                    result *= self.matrix[start_card + w][h]
                    if result == 1:
                        match_cards.append(start_card + w)
                    else:
                        return None
                else:
                    return None

        if result == 1:
            return Cards(match_cards)
        else:
            return None

    # single
    def match_1x1(self, start_card):
        return self.match(start_card, [[1]])

    # pair
    def match_1x2(self, start_card):
        return self.match(start_card, [[1] * 2])

    # triple
    def match_1x3(self, start_card):
        return self.match(start_card, [[1] * 3])

    # bomb
    def match_1x4(self, start_card):
        return self.match(start_card, [[1] * 4])

    # straight 5
    def match_5x1(self, start_card):
        return self.match(start_card, 5 * [[1]])

    # straight 6
    def match_6x1(self, start_card):
        return self.match(start_card, 6 * [[1]])

    # straight 7
    def match_7x1(self, start_card):
        return self.match(start_card, 7 * [[1]])

    # straight 8
    def match_8x1(self, start_card):
        return self.match(start_card, 8 * [[1]])

    # straight 9
    def match_9x1(self, start_card):
        return self.match(start_card, 9 * [[1]])

    # straight 10
    def match_10x1(self, start_card):
        return self.match(start_card, 10 * [[1]])

    # straight 11
    def match_11x1(self, start_card):
        return self.match(start_card, 11 * [[1]])

    # straight 12
    def match_12x1(self, start_card):
        return self.match(start_card, 12 * [[1]])

    # pair straight 3
    def match_3x2(self, start_card):
        return self.match(start_card, 3 * [[1] * 2])

    # pair straight 4
    def match_4x2(self, start_card):
        return self.match(start_card, 4 * [[1] * 2])

    # pair straight 5
    def match_5x2(self, start_card):
        return self.match(start_card, 5 * [[1] * 2])

    # pair straight 6
    def match_6x2(self, start_card):
        return self.match(start_card, 6 * [[1] * 2])

    # pair straight 7
    def match_7x2(self, start_card):
        return self.match(start_card, 7 * [[1] * 2])

    # pair straight 8
    def match_8x2(self, start_card):
        return self.match(start_card, 8 * [[1] * 2])

    # pair straight 9
    def match_9x2(self, start_card):
        return self.match(start_card, 9 * [[1] * 2])

    # pair straight 10
    def match_10x2(self, start_card):
        return self.match(start_card, 10 * [[1] * 2])

    # triple straight 2
    def match_2x3(self, start_card):
        return self.match(start_card, 2 * [[1] * 3])

    # triple straight 3
    def match_3x3(self, start_card):
        return self.match(start_card, 3 * [[1] * 3])

    # triple straight 4
    def match_4x3(self, start_card):
        return self.match(start_card, 4 * [[1] * 3])

    # triple straight 5
    def match_5x3(self, start_card):
        return self.match(start_card, 5 * [[1] * 3])

    # triple straight 6
    def match_6x3(self, start_card):
        return self.match(start_card, 6 * [[1] * 3])

    # random pick a match
    def match_random(self, start_card):
        random_num = random.randint(0, 24)
        return self.match_func_list[random_num](start_card)

    def get_a_randowm_combo(self, combo):
        if self.to_cards().size() == 0:
            return combo
        if len(combo) >= self.current_best_combo_length:
            return None
        cards = self.match_random(self.to_cards()[0])
        if cards is not None:
            combo.append(cards)
            return self.delete(cards).get_a_randowm_combo(combo)
        else:
            return self.get_a_randowm_combo(combo)

    def get_best_combos(self):
        self.current_best_combo_length = 100
        best_combos = []
        combos = []

        # decrease current_best_combo_length
        for i in range(100):
            combo = self.get_a_randowm_combo([])
            if combo is None:
                continue
            if len(combo) <= self.current_best_combo_length:
                self.current_best_combo_length = len(combo)

        for i in range(100):
            combo = self.get_a_randowm_combo([])
            if combo is None:
                continue
            if len(combo) <= self.current_best_combo_length:
                self.current_best_combo_length = len(combo)
                combos.append(combo)

        for combo in combos:
            if len(combo) == self.current_best_combo_length:
                best_combos.append(combo)

        return remove_dup_combo(best_combos)


def get_best_combos(cards, pool, lock):
    matrix = Matrix(cards)
    combos = matrix.get_best_combos()
    lock.acquire()
    pool += combos
    lock.release()


def multi_process_get_best_combos(cards):
    best_combos_pool = multiprocessing.Manager().list()
    best_combos_pool_lock = multiprocessing.Lock()
    process_list = []

    for i in range(4):
        process = multiprocessing.Process(target=get_best_combos, args=(cards, best_combos_pool, best_combos_pool_lock))
        process.start()
        process_list.append(process)

    for process in process_list:
        process.join()

    best_combos_pool = remove_dup_combo(best_combos_pool)

    final_combos = []
    shortest_combos_length = 100
    for combo in best_combos_pool:
        if len(combo) < shortest_combos_length:
            shortest_combos_length = len(combo)

    for combo in best_combos_pool:
        if len(combo) == shortest_combos_length:
            final_combos.append(combo)

    '''
    for combo in final_combos:
        for cards in combo:
            cards.show('')
            print(' ', end='')
        print('')
    '''
    return final_combos


if __name__ == '__main__':
    cards = Cards('344555666677779910JQKKKA22BR')
    multi_process_get_best_combos(cards)
