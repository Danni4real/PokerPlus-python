import sys

from Poker.ai import ai_play, ai_follow
from Poker.cards import Cards, DECK


EMPTY_LIST = []


def wait_for_input():
    return input("Play: ")


if __name__ == '__main__':
    deck = Cards(list(DECK))
    deck.shuffle()
    johns = Cards(deck[0:17])
    marys = Cards(deck[17:34])
    lords = Cards(deck[34:54])

    current_player = lords
    current_cards = EMPTY_LIST
    continuous_pass_times = 0

    while True:
        current_player.show()

        while True:
            if current_player != lords:
                if current_cards == EMPTY_LIST:
                    ai_played_cards = ai_play(current_player)
                    input_string = ai_played_cards.to_str()
                else:
                    ai_played_cards = ai_follow(current_player, current_cards)
                    input_string = ai_played_cards.to_str()
                if len(input_string) != 0:
                    print("Play:", input_string)
            else:
                input_string = wait_for_input()
            if len(input_string) == 0 and current_cards == EMPTY_LIST:
                print("Can't pass, try again!")
                continue
            elif len(input_string) == 0:
                print("Pass!")
                continuous_pass_times += 1
                if continuous_pass_times == 2:
                    continuous_pass_times = 0
                    current_cards = EMPTY_LIST
                break

            input_cards = Cards(input_string)
            if not current_player.contain(input_cards):
                print("Play cards in your hand, try again!")
                continue

            if not input_cards.have_pattern():
                print("Invalid pattern, try again!")
                continue

            if current_cards == EMPTY_LIST:
                pass
            elif input_cards.bigger_than(current_cards):
                pass
            else:
                print("Play bigger than", current_cards.to_str(), "try again!")
                continue

            current_player.delete(input_cards)
            if current_player.size() == 0:
                print("Have a Winner, game over!")
                sys.exit()

            current_cards = input_cards
            continuous_pass_times = 0
            break

        if current_player == lords:
            current_player = johns
        elif current_player == johns:
            current_player = marys
        elif current_player == marys:
            current_player = lords
