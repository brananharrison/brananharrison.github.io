import random
import numpy
from colorama import Fore


def deal(deck):
    card = random.choice(deck)
    deck = deck.remove(card)
    return card


def playerhit(player_hand, value):
    global player_value
    player_hand.append(deal(cards))
    player_value = value + dict.get(player_hand[len(player_hand) - 1])


def dealerhit(player_hand, value):
    global dealer_value
    player_hand.append(deal(cards))
    dealer_value = value + dict.get(player_hand[len(player_hand) - 1])


def numaces(player_hand):
    count = 0
    for i in range(len(player_hand)):
         if player_hand[i][0] == 'A':
             count = count + 1
    return count


def get_bet():
    global bet, min_bet
    parsed = False
    while not parsed:
        try:
            bet = int(input(Fore.LIGHTRED_EX + 'Enter bet: '))
            while bet > balance:
                print('Your bet exceeds your balance! Try lowering your bet.')
                bet = int(input(Fore.LIGHTRED_EX + 'Enter bet: '))
            while bet < min_bet and bet != 0:
                print('Your bet does not meet the house minimum.')
                bet = int(input(Fore.LIGHTRED_EX + 'Enter bet: '))
            parsed = True
        except ValueError:
            print('Please enter a numeric value.')


def shuffle():
    global cards, num_decks
    cards = ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS',
             'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC',
             'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD',
             'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH']
    return cards


def soft_check():
    global player_value, player_hand
    if playerfunction() >= 21:
        return ''
    else:
        if numaces(player_hand) == 0:
            return 'hard'
        for i in range(1, 10):
            if numaces(player_hand) == i and player_value - 10*i == playerfunction():
                return 'hard'
            else:
                return 'soft'


def cut_deck():
    global cards, num_decks, cut
    parsed = False
    cards = cards * num_decks
    min_cut = int(numpy.rint(0.25 * len(cards)))
    max_cut = int(numpy.rint(0.95 * len(cards)))
    while not parsed:
        try:
            print(Fore.BLUE + 'Choose a place to cut the deck between', min_cut, 'and', max_cut, ': ')
            cut = int(input())
            if min_cut <= cut <= max_cut:
                parsed = True
            else:
                print(Fore.LIGHTMAGENTA_EX + 'Please choose a position inside of the range.')
        except ValueError:
            print(Fore.LIGHTMAGENTA_EX + 'Please enter a numeric value.')
    return cut


def hit():
    global player_hand, player_value, turn, balance
    playerhit(player_hand, player_value)
    print(Fore.WHITE + 'You got a', Fore.LIGHTYELLOW_EX + player_hand[len(player_hand) - 1],
          Fore.WHITE + 'for a total of' + Fore.LIGHTYELLOW_EX, soft_check(), playerfunction())
    if playerfunction() > 21:
        print(Fore.WHITE + 'You have' + Fore.LIGHTYELLOW_EX, playerfunction())
        print(Fore.LIGHTMAGENTA_EX + 'You bust!')
        balance = balance - min_bet
    if playerfunction() == 21:
        print(Fore.LIGHTMAGENTA_EX + 'You got 21!')
        if splitlock == False:
            if dealerfunction() == 21:
                print(Fore.LIGHTRED_EX + 'Dealer also has 21. Push!')
            else:
                print(Fore.LIGHTRED_EX + 'Dealer has', dealerfunction(), Fore.LIGHTMAGENTA_EX + 'You win!')
                balance = balance + bet


def stand():
    global player_value, player_hand, turn, balance
    if splitlock == False:
        print(Fore.LIGHTGREEN_EX + 'You have', playerfunction())
        print(Fore.LIGHTRED_EX + 'Dealer has', dealer_hand, Fore.WHITE + 'a total of' + Fore.LIGHTRED_EX,
        dealerfunction())
        if playerfunction() > 21:
            print(Fore.LIGHTMAGENTA_EX + 'You bust!')
            balance = balance - min_bet
        if dealerfunction() < playerfunction() <= 21:
            print(Fore.LIGHTMAGENTA_EX + 'You win!')
            balance = balance + min_bet
        if playerfunction() < dealerfunction() <= 21:
            print(Fore.LIGHTMAGENTA_EX + 'You lose!')
            balance = balance - min_bet
        if playerfunction() <= 21 < dealerfunction():
            print(Fore.LIGHTMAGENTA_EX + 'Dealer busts!')
            balance = balance + min_bet
        if playerfunction() == dealerfunction():
            print(Fore.LIGHTMAGENTA_EX + 'Push!')


def double():
    global player_hand, player_value, balance, bet, turn
    playerhit(player_hand, player_value)
    if splitlock == False:
        if playerfunction() > 21:
            print(Fore.WHITE + 'You got a', Fore.LIGHTYELLOW_EX + player_hand[len(player_hand) - 1],
                  Fore.WHITE + 'for a total of' + Fore.LIGHTYELLOW_EX, playerfunction())
            print(Fore.LIGHTMAGENTA_EX + 'You bust!')
            balance = balance - min_bet
        else:
            print(Fore.WHITE + 'You got a', Fore.LIGHTYELLOW_EX + player_hand[len(player_hand) - 1],
                  Fore.WHITE + 'for a total of' + Fore.LIGHTYELLOW_EX, playerfunction())
            print(Fore.WHITE + 'Dealer has' + Fore.LIGHTRED_EX, dealerfunction())
            if playerfunction() == dealerfunction():
                print(Fore.LIGHTMAGENTA_EX + 'Push!')
            if dealerfunction() < playerfunction() <= 21:
                print(Fore.LIGHTMAGENTA_EX + 'You win!')
                balance = balance + bet
            if playerfunction() < dealerfunction() <= 21:
                print(Fore.LIGHTMAGENTA_EX + 'You lose')
                balance = balance - bet
            if dealerfunction() > 21:
                print(Fore.LIGHTMAGENTA_EX + 'Dealer busts!')
                balance = balance + bet
        print('Balance:', balance)
        turn = False


def playerfunction():
    global player_value, player_hand
    if player_value <= 21:
        return player_value
    if player_value > 21:
        if numaces(player_hand) == 0:
            return player_value
        if numaces(player_hand) == 1:
            return player_value - 10
        if numaces(player_hand) == 2:
            if (player_value - 10) <= 21:
                return player_value - 10
            else:
                return player_value - 20
        for i in range(3, 16):
            if numaces(player_hand) == i:
                if (player_value - 10*i) <= 21:
                    return player_value - 10*i
                if (player_value - 10*i) > 21 and numaces(player_hand) == i:
                    return player_value - 10*i


def dealerfunction():
    global dealer_hand, dealer_value
    while dealer_value < 17:
        dealerhit(dealer_hand, dealer_value)
    if 17 <= dealer_value <= 21:
        return dealer_value
    if dealer_value > 21:
        if numaces(dealer_hand) == 0:
            return dealer_value
        if numaces(dealer_hand) == 1:
            if (dealer_value - 10*1) < 17:
                dealerhit(dealer_hand, dealer_value)
            if 17 <= (dealer_value - 10 * 1) <= 21:
                return dealer_value - 10
            if (dealer_value - 10*1) > 21 and numaces(dealer_hand) == 1:
                return dealer_value - 10
        if numaces(dealer_hand) == 2:
            while (dealer_value - 10*1) < 17:
                dealerhit(dealer_hand, dealer_value)
            if 17 <= (dealer_value - 10 * 1) <= 21:
                return dealer_value - 10
            if (dealer_value - 10*1) > 21:
                while (dealer_value - 10*2) < 17:
                    dealerhit(dealer_hand, dealer_value)
                if 17 <= (dealer_value - 10 * 2) <= 21:
                    return dealer_value - 20
                if (dealer_value - 10*2) > 21 and numaces(dealer_hand) == 2:
                    return dealer_value - 20
        for i in range(3, 16):
            if numaces(dealer_hand) == i:
                while (dealer_value - 10*i) < 17:
                    dealerhit(dealer_hand, dealer_value)
                if 17 <= (dealer_value - 10*i) <= 21:
                    return dealer_value - 10*i
                if (dealer_value - 10*i) > 21 and numaces(dealer_hand) == i:
                    return dealer_value - 10*i


cards = ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS',
         'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC',
         'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD',
         'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH']
dict = {'AS': 11, '2S': 2, '3S': 3, '4S': 4, '5S': 5, '6S': 6, '7S': 7, '8S': 8, '9S': 9, '10S': 10,
        'JS': 10, 'QS': 10, 'KS': 10, 'AC': 11, '2C': 2, '3C': 3, '4C': 4, '5C': 5, '6C': 6, '7C': 7,
        '8C': 8, '9C': 9, '10C': 10, 'JC': 10, 'QC': 10, 'KC': 10, 'AD': 11, '2D': 2, '3D': 3, '4D': 4,
        '5D': 5, '6D': 6, '7D': 7, '8D': 8, '9D': 9, '10D': 10, 'JD': 10, 'QD': 10, 'KD': 10, 'AH': 11,
        '2H': 2, '3H': 3, '4H': 4, '5H': 5, '6H': 6, '7H': 7, '8H': 8, '9H': 9, '10H': 10, 'JH': 10,
        'QH': 10, 'KH': 10}

# Game Rules:
num_decks = int(input('Enter number of decks: '))
balance = int(input('Enter starting balance: '))
min_bet = int(input('Enter minimum bet: '))
play_again = True
cut = cut_deck()

while play_again:
    if balance < min_bet:
        print(Fore.LIGHTMAGENTA_EX + 'You ran out of money!')
        break
    if len(cards) < cut:
        print(Fore.LIGHTMAGENTA_EX + 'Dealer shuffles.')
        shuffle()
        cut = cut_deck()

    get_bet()
    if bet == 0:
        print(Fore.LIGHTMAGENTA_EX + 'Thanks for playing!')
        break

    turn = True
    double_option = True

    # Initial deal
    player_hand = ['KS']
    dealer_hand = [deal(cards)]
    player_hand.append('10S')
    dealer_hand.append(deal(cards))

    # Calculating values
    dealer_value = dict.get(dealer_hand[0]) + dict.get(dealer_hand[1])
    player_value = dict.get(player_hand[0]) + dict.get(player_hand[1])

    # Printing cards to player
    print(Fore.WHITE + 'You have', Fore.LIGHTYELLOW_EX + player_hand[0], Fore.WHITE + 'and', Fore.LIGHTYELLOW_EX + player_hand[1])
    print(Fore.WHITE + 'The dealer has', Fore.LIGHTRED_EX + dealer_hand[0], Fore.WHITE + 'showing.')

    # Player turn
    while turn:
        if playerfunction() == 21 and len(player_hand) == 2:
            print(Fore.LIGHTMAGENTA_EX + 'Blackjack!')
            if dealerfunction() == 21:
                print(Fore.LIGHTRED_EX + 'Dealer also has blackjack. Push!')
            else:
                print(Fore.WHITE + 'Dealer got a total of', dealerfunction())
                balance = balance + bet * 1.5
                print(Fore.LIGHTMAGENTA_EX + 'Balance:', balance)
            turn = False
        else:
            if dict.get(player_hand[0]) == dict.get(player_hand[1]):
                player_choice = input(Fore.WHITE + 'Hit, stand, split, or double? (H, S, P, D): ')
            if dict.get(player_hand[0]) != dict.get(player_hand[1]) and double_option == True:
                player_choice = input(Fore.WHITE + 'Hit, stand, or double? (H, S, D): ')
            if not double_option:
                player_choice = input(Fore.WHITE + 'Hit, or stand? (H, S): ')
            if player_choice == 'D':
                if double_option:
                    double()
                else:
                    print('You cannot double after hitting!')
            if player_choice == 'H':
                hit()
                if playerfunction() >= 21:
                    print('Balance:', balance)
                    turn = False
                double_option = False
            if player_choice == 'S':
                stand()
                if splitlock == False:
                    print('Balance:', balance)
                    turn = False
            if player_choice == 'P':
                if balance - bet*2 > 0:
                    splitcounter = 0
                    split_value = []
                    splitlock = True
                    turn = False
                else:
                    print(Fore.LIGHTMAGENTA_EX + 'You dont have enough money to split!')

    while splitlock:
        if splitcounter == 0:
            left_split = player_hand[0]
            right_split = player_hand[1]
            left_new = deal(cards)
            player_hand = [left_split, left_new]
            player_value = dict.get(left_split) + dict.get(left_new)

            print(Fore.WHITE + 'Your first hand was delt a' + Fore.LIGHTYELLOW_EX, left_new,
              Fore.WHITE + 'for a total of' + Fore.LIGHTYELLOW_EX, playerfunction())
        if splitcounter == 1:
            right_new = deal(cards)
            player_hand = [right_split, right_new]
            player_value = dict.get(player_hand[0]) + dict.get(player_hand[1])
            print(Fore.WHITE + 'Your second hand was delt a' + Fore.LIGHTYELLOW_EX, player_hand[1],
              Fore.WHITE + 'for a total of' + Fore.LIGHTYELLOW_EX, soft_check(), playerfunction())

        if dict.get(player_hand[0]) == dict.get(player_hand[1]):
            player_choice = input(Fore.WHITE + 'Hit, stand, split, or double? (H, S, P, D): ')
        if dict.get(player_hand[0]) != dict.get(player_hand[1]) and double_option == True:
            player_choice = input(Fore.WHITE + 'Hit, stand, or double? (H, S, D): ')
        if player_choice == 'H':
            hit()
            if playerfunction() >= 21:
                split_value.append(playerfunction())
                splitcounter = splitcounter + 1
        if player_choice == 'S':
            stand()
            split_value.append(playerfunction())
            splitcounter = splitcounter + 1
        if player_choice == 'D':
            double()
            print(Fore.WHITE + 'You got a', Fore.LIGHTYELLOW_EX + player_hand[len(player_hand) - 1],
                  Fore.WHITE + 'for a total of' + Fore.LIGHTYELLOW_EX, playerfunction())
            splitcounter = splitcounter + 1
            split_value.append(playerfunction())
        if player_choice == 'P':
            print(Fore.RED + 'I forbid you from splitting twice.')

        if splitcounter == 2:
            print(Fore.WHITE + 'Dealer has' + Fore.LIGHTRED_EX, dealerfunction())
            if dealerfunction() > 21:
                print(Fore.LIGHTMAGENTA_EX + 'Dealer busts!')
                for i in range(0, 2):
                    if i == 0:
                        if split_value[i] > 21:
                            print(Fore.LIGHTRED_EX + 'Your first hand busted!')
                            balance = balance - bet
                        if split_value[i] <= 21:
                            print(Fore.LIGHTGREEN_EX + 'Your first hand wins!')
                            balance = balance + bet
                    if i == 1:
                        if split_value[i] > 21:
                            print(Fore.LIGHTRED_EX + 'Your second hand busted!')
                            balance = balance - bet
                        if split_value[i] <= 21:
                            print(Fore.LIGHTGREEN_EX + 'Your second hand wins!')
                            balance = balance + bet
            else:
                for i in range(0, 2):
                    if i == 0:
                        if split_value[i] > 21:
                            print(Fore.LIGHTRED_EX + 'Your first hand busted!')
                            balance = balance - bet
                        if dealerfunction() < split_value[i] <= 21:
                            print(Fore.LIGHTGREEN_EX + 'Your first hand won!')
                            balance = balance + min_bet
                        if split_value[i] < dealerfunction() <= 21:
                            print(Fore.LIGHTRED_EX + 'Your first hand lost!')
                            balance = balance - min_bet
                        if split_value[i] == dealerfunction() <= 21:
                            print(Fore.LIGHTMAGENTA_EX + 'Your first hand pushes!')
                    if i == 1:
                        if split_value[i] > 21:
                            print(Fore.LIGHTRED_EX + 'Your second hand busted!')
                            balance = balance - bet
                        if dealerfunction() < split_value[i] <= 21:
                            print(Fore.LIGHTGREEN_EX + 'Your second hand won!')
                            balance = balance + min_bet
                        if split_value[i] < dealerfunction() <= 21:
                            print(Fore.LIGHTRED_EX + 'Your second hand lost!')
                            balance = balance - min_bet
                        if split_value[i] == dealerfunction() <= 21:
                            print(Fore.LIGHTMAGENTA_EX + 'Your second hand pushes!')
            print('Balance:', balance)
            splitlock = False



