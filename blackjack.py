# This program will execute a simplified version of the game Blackjack
# Language:Python 3.7.4
# Programmer: Noah Khan
# blackjack.py

from random import shuffle


# I'm creating a table class where the rest of the objects will reside to play the game
# this will allow different objects to interact with each other 'on the table'
class Table(object):

    def __init__(self, player):

        self.dealer = Dealer()
        self.player = Player(player)
        self.deck = Deck()

        # call table_setup() method to shuffle and deal first cards
        self.table_setup()

    def table_setup(self):

        # shuffle the deck before dealing each game
        self.deck.shuffle()


        # deal a card to the player, then the dealer, then the player to start the game
        self.deal_card(self.player)
        self.deal_card(self.dealer)
        self.deal_card(self.player)
        self.calculate_score(self.player)  # calculate the player and dealer score at start to check for blackjack
        self.calculate_score(self.dealer)

        # call self.main() which is where we will set up the recurring hit/stick prompt and deal cards
        self.main()

    def main(self):

        while True:
            print()
            print(self)
            player_move = self.player.hit_or_stick()
            if player_move is True:
                self.deal_card(self.player)
                self.calculate_score(self.player)
            elif player_move is False:
                self.dealer_hit()

    def dealer_hit(self):

        score = self.dealer.score
        while True:
            if score < 17:
                self.deal_card(self.dealer)
                self.calculate_score(self.dealer)
                print(self)
            elif score >= 17:
                self.check_final_score()

    def __str__(self):  # this is just for checking progress during programming

        dealer_hand = [card for card, value in self.dealer.hand]
        player_hand = [card for card, value in self.player.hand]

        print("Dealer hand : {}".format(dealer_hand))
        print("Dealer score : {}".format(self.dealer.score))
        print()
        print("{}'s hand : {}".format(self.player.name, player_hand))
        print("{}'s score : {}".format(self.player.name, self.player.score))
        print("-" * 40)
        return ''

    def deal_card(self, player):

        card = self.deck.stack.pop()
        player.hand.append(card)

    def calculate_score(self, player):

        ace = False  # figure a way to check for ace in hand
        score = 0
        for card in player.hand:
            if card[1] == 1 and not ace:
                ace = True
                card = ('A', 11)
            score += card[1]
        player.score = score
        if player.score > 21 and ace:
            player.score -= 10
            score = player.score
        self.check_win(score, player)
        return

    def check_win(self, score, player):
        if score > 21:
            print()
            print(self)
            print("{} busts".format(player.name))
            print()
            self.end_game()
        elif score == 21:
            print(self)
            print("{} blackjack!".format(player.name))
            self.end_game()
        else:
            return

    def check_final_score(self):

        dealer_score = self.dealer.score
        player_score = self.player.score

        if dealer_score > player_score:
            print("Dealer wins!")
            self.end_game()
        else:
            print("{} wins!".format(self.player.name))
            self.end_game()

    def end_game(self):

        again = input("Do you want to play again (Y/N)? ")
        if again.lower().startswith('y'):
            self.__init__(self.player.name)
        elif again.lower().startswith('n'):
            exit()


class Dealer(object):

    def __init__(self):

        self.name = "Dealer"
        self.score = 0
        self.hand = []


class Player(Dealer):

    def __init__(self, name):
        super().__init__()
        self.name = name

    @staticmethod
    def hit_or_stick():
        while True:
            choice = input("Do you want another card (Y/N)? ")
            if choice.lower().startswith('y'):
                return True
            elif choice.lower().startswith('n'):
                return False
            else:
                print("I didn't understand")
                continue


class Deck(object):

    # create a list of all the values and shuffle them
    # when dealing the cards use pop() to get the card off the top of the stack

    def __init__(self):

        # stack is composed of tuples:
        # [0] is a string to show the player for their hand
        self.stack = [('A', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
                      ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10),
                      ('J', 10), ('Q', 10), ('K', 10)] * 4
        self.shuffle()

    def shuffle(self):

        shuffle(self.stack)

    def deal_card(self):

        card = self.stack.pop()
        return card


def main():

    player_name = input("Enter your name: ")
    Table(player_name)


if __name__ == '__main__':

    main()