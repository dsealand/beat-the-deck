import pyCardDeck
from typing import List
from pyCardDeck.cards import PokerCard
import math
import random

class BeatTheDeck:
    def __init__(self):
        self.deck = pyCardDeck.Deck(
            cards=generate_deck(),
            name='Poker deck',
            reshuffle=False)
        self.board = []
        self.scores = {}
        print("Created a game.")

    def deal_board(self):
        """
        Deal a board (9 initial card stacks)
        """
        for i in range(9):
            self.board.append([self.deck.draw()])
            print(i, ": ", self.board[i])

    def beat_the_deck(self):
        """
        The main beat the deck game sequence.
        """
        print("Setting up...")
        print("Shuffling...")
        self.deck.shuffle()
        print("All shuffled!")
        print("Dealing...")
        self.deal_board()
        while True:
            self.turn()
            if self.deck.cards_left == 0:
                print("You win!")
                return 1, 0
            elif len(self.board) == 0:
                print("You lose...")
                return 0, self.deck.cards_left

    def turn(self):
        """
        Play one turn.
        """
        # stack, choice = self.hardFirst()
        stack, choice = self.naive()
        # stack, choice = self.random()

        print("stack and choice: ", stack, choice)

        card = self.deck.draw()

        if is_valid(card, self.board[stack], choice):
            self.board[stack].insert(0, card)
            print("Placed ", card.name, " on stack: ", self.board[stack])
        else:
            print("Unlucky. Card:", card, "Choice:", choice, "Stack:", self.board[stack])
            self.board.pop(stack)

        for index, stack in enumerate(self.board):
            print(index, ": ", stack[0])
        print("Cards left: ", self.deck.cards_left)

    def naive(self):
        """
        Play with naive strategy - best odds (highest/lowest visible card)
        """
        bestStackValue = -math.inf
        bestStackIndex = None
        for index, stack in enumerate(self.board):
            stackValue = abs(7.5-int(stack[0].rank))
            if stackValue > bestStackValue:
                bestStackValue = stackValue
                bestStackIndex = index
        
        if int(self.board[bestStackIndex][0].rank) > 7.5:
            choice = 0
        else:
            choice = 2
        
        return bestStackIndex, choice

    def hardFirst(self):
        """
        Play hardest (7s/8s) first.
        """
        bestStackValue = math.inf
        bestStackIndex = None
        for index, stack in enumerate(self.board):
            stackValue = abs(7.5-int(stack[0].rank))
            if stackValue < bestStackValue:
                bestStackValue = stackValue
                bestStackIndex = index
        
        if int(self.board[bestStackIndex][0].rank) > 7.5:
            choice = 0
        else:
            choice = 2

        return bestStackIndex, choice

    def random(self):
        """
        Select a random stack and over/under choice.
        """
        stack = random.randint(0, len(self.board)-1)
        if int(self.board[stack][0].rank) > 7.5:
            choice = 0
        else:
            choice = 2
        return stack, choice


def is_valid(card, stack, choice):
    """
    Determine if placing drawn card on stack with choice of over/under/on is valid.
    """
    stack_rank = int(stack[0].rank)
    if (int(card.rank) < stack_rank) and (choice == 0):
        return True
    elif (int(card.rank) == stack_rank) and (choice == 1):
        return True
    elif (int(card.rank) > stack_rank) and (choice == 2):
        return True
    else:
        return False

def generate_deck() -> List[PokerCard]:
    """
    Function that generates the deck, instead of writing down 50 cards, we use iteration
    to generate the cards for use
    :return:    List with all 50 poker playing cards
    :rtype:     List[PokerCard]
    """
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = {'1': 'Ace',
             '2': 'Two',
             '3': 'Three',
             '4': 'Four',
             '5': 'Five',
             '6': 'Six',
             '7': 'Seven',
             '8': 'Eight',
             '9': 'Nine',
             '10': 'Ten',
             '11': 'Jack',
             '12': 'Queen',
             '13': 'King'}
    cards = []
    for suit in suits:
        for rank, name in ranks.items():
            cards.append(PokerCard(suit, rank, name))
    print('Generated deck of cards for the table')
    return cards

if __name__ == "__main__":
    games = 10000
    totalCardsLeft = 0
    wins = 0
    for i in range(games):
        game = BeatTheDeck()
        score, cardsLeft = game.beat_the_deck()
        totalCardsLeft += cardsLeft
        if score == 1:
            wins += 1
    print(wins, " out of ", games, " games")
    print("average number of cards left in losses", totalCardsLeft/(games-wins))