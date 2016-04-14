# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
message = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
    def draw_back(self, canvas, pos):
        card_loc = (CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0], CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
# define hand class

class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []
        
    def __str__(self):
        # return a string representation of a hand
        cardhand = ""
        for i in self.hand:
            cardhand += str(i) + " "
        return ""
    
    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        is_ace = False
        for i in self.hand:
            cardrank = i.get_rank()
            value += VALUES[cardrank]
            if cardrank == "A":
                is_ace = True
        if is_ace and value + 10 <= 21:
            return value + 10
        else:
            return value
                         
    def draw(self, canvas, pos):
    # draw a hand on the canvas, use the draw method for cards
        for i in self.hand:
            pos[0] = pos[0] + CARD_SIZE[0] + 5
            i.draw(canvas, pos)
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        return [self.deck.append(Card(n, i)) for n in SUITS for i in RANKS]
       
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)
        
    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        carddeck = ""
        for i in self.deck:
            carddeck += str(i) + " "
        return "Deck contains " + carddeck

#define event handlers for buttons
def deal():
    global outcome, in_play, dealerhand, playerhand, newdeck, score, message
    if in_play:
        in_play = False
        score -= 1
        message = "You lost the round"
        deal()
    else:
        newdeck = Deck()
        newdeck.shuffle()
        dealerhand = Hand()
        playerhand = Hand()
        dealerhand.add_card(newdeck.deal_card()) 
        dealerhand.add_card(newdeck.deal_card())
        playerhand.add_card(newdeck.deal_card())
        playerhand.add_card(newdeck.deal_card())
        #print "Dealer " + str(dealerhand) 
        #print "Player " + str(playerhand)
        outcome = "Hit or Stand?"
        message = ""
        in_play = True
        
def hit():
    global playerhand, in_play, outcome, newdeck, score, message
    if in_play:
        if playerhand.get_value() <= 21:
            playerhand.add_card(newdeck.deal_card())
            if playerhand.get_value() > 21: 
                message = "You have busted"
                in_play = False
                score -= 1
                outcome = "New deal?"
        
def stand():
    global playerhand, dealerhand, newdeck, in_play, outcome, score, message
    if in_play:
        if playerhand.get_value() > 21:
            message = "You have busted"       
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealerhand.get_value() < 17:
            dealerhand.add_card(newdeck.deal_card())
        # assign a message to outcome, update in_play and score
        if dealerhand.get_value() > 21:
            message = "Dealer has busted"
            score += 1
        elif playerhand.get_value() > dealerhand.get_value():
            message = "You win"
            score += 1
        else:
            message = "You loose"
            score -= 1
        outcome = "New deal?"
        in_play = False
        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BLACKJACK", (160, 80), 48, "Black")
    canvas.draw_text(message, (200, 150), 30, "Red", "sans-serif")
    canvas.draw_text("Score: " + str(score), (490, 30), 24, "White", "sans-serif")
    canvas.draw_text(outcome, (250, 550), 24, "White", "sans-serif")
    canvas.draw_text("Player", (15, 450), 18, "White", "sans-serif")
    canvas.draw_text("Dealer", (15, 250), 18, "White", "sans-serif")
    playerhand.draw(canvas, [30, 400])
    dealerhand.draw(canvas, [30, 200])
    if in_play:
        dealerhand.hand[0].draw_back(canvas, [106, 200])
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric