from operator import itemgetter

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
class Card:

    def __init__(self, symbol):
        self.value = cardvalues[symbol]
        self.symbol = symbol

    def __lt__(self,other):
        return self.value<other.value
    def __repr__(self):
        return str(self.symbol)



cards = {}

for k, v in cardvalues.items():
    cards[k] = Card(k)

def getcard(k):
    return cards[k]

class Hand:

    def setJoker():
        cards['J'].value=1

    def unsetJoker():
        cards['J'].value=11

    def getJoker():
        return cards['J'].value==1
    def __init__(self,handsymbols):
        self.hand=[]
        for symbol in handsymbols:
            self.hand.append(getcard(symbol))
        self.uniquecards=set(self.hand)

    '''
    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards'
    '''
    def isxofakind(self,x):

        if len(self.uniquecards)==1 and x==5:
            return True
        for a in self.uniquecards:
            count=0
            if a.value==1:
                continue
            for b in self.hand:
                if a.value==b.value or b.value==1:
                    count+=1
            if count==x:
                return True
        return False
    def isfullhouse(self):
        a=self.uniquecards
        return len(a)==2 or (len(a)==3 and self.countjoker())

    def istwopairs(self):
        a = self.uniquecards
        return (self.isxofakind(2) and len(a)==3) or (self.countjoker() and len(a)==4)

    def isonepair(self):
        a = self.uniquecards
        return self.isxofakind(2) and len(a)==4 or self.countjoker()

    def countjoker(self):
        if not Hand.getJoker():
            return 0
        countjoker=0
        for card in self.hand:
            if card.value==1:
                countjoker+=1
        return countjoker
    def typevalue(self):
        if self.isxofakind(5):
            return 7e12
        elif self.isxofakind(4):
            return 6e12
        elif self.isfullhouse():
            return 5e12
        elif self.isxofakind(3):
            return 4e12
        elif self.istwopairs():
            return 3e12
        elif self.isonepair():
            return 2e12
        else:
            return 1e12

    def cardvalue(self):
        cardvalue=0
        i=0
        while i<5:
            cardvalue=cardvalue*100+self.hand[i].value
            i+=1
        return cardvalue

    def value(self):
            return self.typevalue()+self.cardvalue()
    def __lt__(self,other):
        return self.value()<other.value()

    def __repr__(self):
        return str([str(x) for x in self.hand]+[self.value()])



hands=[]
with open("seventh.txt","r") as f:
    for line in f:
        symbols,bid=line.strip().split()
        hands.append([Hand(symbols),int(bid)])

Hand.unsetJoker()
s=0
rank=1
sorted_hands=sorted(hands,key=itemgetter(0))
for hand in sorted_hands:
    s+=rank*hand[1]
    rank+=1

print(s)

Hand.setJoker()
s=0
rank=1
sorted_hands_2=sorted(hands,key=itemgetter(0))
for hand in sorted_hands_2:
    s+=rank*hand[1]
    rank+=1

print(s)

