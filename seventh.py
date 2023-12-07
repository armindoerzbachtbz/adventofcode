from operator import itemgetter

'''
This Card object implements a simple Card with the Symbol and value of the card
'''
class Card:
    def __init__(self, symbol,value):
        self.value = value
        self.symbol = symbol

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return str(self.symbol)

'''
This is the static class containing all Card Objects.
'''
class Cards:
    cards = {}
    cardvalues = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 1,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    for k, v in cardvalues.items():
        cards[k] = Card(k,v)

    def getcard(k):
        return Cards.cards[k]


'''
This Class implements all the stuff to compare and store a Hand.
'''
class Hand:

    def setJoker():
        Cards.cards['J'].value = 1

    def unsetJoker():
        Cards.cards['J'].value = 11

    def withJoker():
        return Cards.cards['J'].value == 1

    def __init__(self, handsymbols):
        self.hand = []
        for symbol in handsymbols:
            self.hand.append(Cards.getcard(symbol))
        self.uniquecards = set(self.hand)



    '''
    Checks if there are x similiar Cards.
    if J is a Jocker this is also taken into account.
    '''
    def isxofakind(self, x):

        if len(self.uniquecards) == 1 and x == 5:
            return True
        for a in self.uniquecards:
            count = 0
            if a.value == 1:
                continue
            for b in self.hand:
                if a.value == b.value or b.value == 1:
                    count += 1
            if count == x:
                return True
        return False

    def isfullhouse(self):
        a = self.uniquecards
        return len(a) == 2 or (len(a) == 3 and self.countjoker())

    def istwopairs(self):
        a = self.uniquecards
        return (self.isxofakind(2) and len(a) == 3) or (self.countjoker() and len(a) == 4)

    def isonepair(self):
        a = self.uniquecards
        return self.isxofakind(2) and len(a) == 4 or self.countjoker()

    def countjoker(self):
        if not Hand.withJoker():
            return 0
        countjoker = 0
        for card in self.hand:
            if card.value == 1:
                countjoker += 1
        return countjoker

    '''
    Returns the typevalue of the hand which is
   
    7000000000000: Five of a kind, where all five cards have the same label: AAAAA
    6000000000000: Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    5000000000000: Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    4000000000000: Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    3000000000000: Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    2000000000000: One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    1000000000000: High card, where all cards'
    
    
    '''
    def typevalue(self):
        if self.isxofakind(5):
            return int(7e12)
        elif self.isxofakind(4):
            return int(6e12)
        elif self.isfullhouse():
            return int(5e12)
        elif self.isxofakind(3):
            return int(4e12)
        elif self.istwopairs():
            return int(3e12)
        elif self.isonepair():
            return int(2e12)
        else:
            return int(1e12)

    '''
    Returns the value of the Cards in the right order:
    aabbccddee
    
    aa: is two digits for the first card of the hand
    bb: is two digits for the second card of the hand
    ...
    
    -> Comparing of the value is simple
    '''
    def cardvalue(self):
        cardvalue = 0
        i = 0
        while i < 5:
            cardvalue = cardvalue * 100 + self.hand[i].value
            i += 1
        return cardvalue

    '''
    Returns the value of the card which is the sum of the typevalue and the cardvalue.
    '''
    def value(self):
        return self.typevalue() + self.cardvalue()

    def __lt__(self, other):
        return self.value() < other.value()

    def __repr__(self):
        return str([str(x) for x in self.hand] + [self.value()])


hands = []
with open("seventh.txt", "r") as f:
    for line in f:
        symbols, bid = line.strip().split()
        hands.append([Hand(symbols), int(bid)])

Hand.unsetJoker()
s1 = 0
rank = 1
sorted_hands = sorted(hands, key=itemgetter(0))
for hand in sorted_hands:
    s1 += rank * hand[1]
    rank += 1
print("Part1 ==============")
print(sorted_hands[:5])
print(sorted_hands[-5:])
print("Part1 ==============")

Hand.setJoker()
s = 0
rank = 1
sorted_hands_2 = sorted(hands, key=itemgetter(0))
for hand in sorted_hands_2:
    s += rank * hand[1]
    rank += 1
print("Part2 ==============")
print(sorted_hands_2[:5])
print(sorted_hands_2[-5:])
print("Part2 ==============")
print("Solution Part1: %d"%s1)
print("Solution Part2: %d"%s)

