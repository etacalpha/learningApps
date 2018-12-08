import tkinter
import random


def loadImages(cardImages):
    suits = ['heart', 'club', 'diamond', 'spade']
    faceCards = ['jack', 'queen', 'king']

    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'

    # for each suit retrieve the image for the cards
    for suit in suits:
        for card in range(1, 11):
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            cardImages.append((card, image,))

        # face cards
        for card in faceCards:
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            cardImages.append((10, image,))


def dealCard(frame):
    # pop next card from deck
    nextCard = deck.pop(0)
    # add it back to deck
    deck.append(nextCard)
    # add image to label and display
    tkinter.Label(frame, image=nextCard[1], relief='raised').pack(side='left')
    # return cards face value
    return nextCard


def dealDealer():
    dealerScore = scoreHand(dealerHand)
    while 0 < dealerScore < 17:
        dealerHand.append(dealCard(dealerCardFrame))
        dealerScore = scoreHand(dealerHand)
        dealerScoreLabel.set(dealerScore)

    playerScore = scoreHand(playerHand)
    if playerScore > 21:
        resultText.set("Dealer Wins !!")
    elif dealerScore > 21 or dealerScore < playerScore:
        resultText.set("Player wins!!")
    elif dealerScore > playerScore:
        resultText.set("Dealer Wins !!")
    elif dealerScore == playerScore:
        resultText.set("Draw")


def dealPlayer():
    playerHand.append(dealCard(playerCardFrame))
    playerScore = scoreHand(playerHand)

    playerScoreLabel.set(playerScore)
    if playerScore > 21:
        resultText.set("Dealer Wins!!")


def scoreHand(hand):
    # Calculate total score of all cards in the list.
    # Only one ace can have the value 11, and this will be reduced to 1 if the hand would bust
    score = 0
    ace = False
    for nextCard in hand:
        cardValue = nextCard[0]
        if cardValue == 1 and not ace:
            ace = True
            cardValue = 11
        score += cardValue
        # if bust check for ace and subtract 10 if true
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def initDeal():
    dealPlayer()
    dealerHand.append(dealCard(dealerCardFrame))
    dealerScoreLabel.set(scoreHand(dealerHand))
    dealPlayer()


def newGame():
    global dealerCardFrame
    global playerCardFrame
    global dealerHand
    global playerHand
    # embedded frame to hold card images
    dealerCardFrame.destroy()
    dealerCardFrame = tkinter.Frame(cardFrame, background="green")
    dealerCardFrame.grid(row=0, column=1, sticky='ew', rowspan='2')

    playerCardFrame.destroy()
    # embedded frame to hold card images
    playerCardFrame = tkinter.Frame(cardFrame, background="green")
    playerCardFrame.grid(row=2, column=1, sticky='ew', rowspan=2)

    resultText.set("")

    # Create list to store dealer and players hands
    dealerHand = []
    playerHand = []

    initDeal()


def shuffle():
    random.shuffle(deck)


def play():
    initDeal()

    mainWindow.mainloop()


mainWindow = tkinter.Tk()

# setup screen and flames for the dealer and player
mainWindow.title("Black Jack")
mainWindow.geometry("640x480")
mainWindow.configure(background="green")

resultText = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=resultText)
result.grid(row=0, column=0, columnspan=3)
cardFrame = tkinter.Frame(mainWindow, relief="sunken", borderwidth=1, background="green")
cardFrame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

dealerScoreLabel = tkinter.IntVar()
tkinter.Label(cardFrame, text="Dealer", background="green", fg="white").grid(row=0, column=0)
tkinter.Label(cardFrame, textvariable=dealerScoreLabel, background="green", fg="white").grid(row=1, column=0)

# embedded frame to hold the card images
dealerCardFrame = tkinter.Frame(cardFrame, background="green")
dealerCardFrame.grid(row=0, column=1, sticky='ew', rowspan='2')

playerScoreLabel = tkinter.IntVar()
tkinter.Label(cardFrame, text="Player", background="green", fg="white").grid(row=2, column=0)
tkinter.Label(cardFrame, textvariable=playerScoreLabel, background="green", fg="white").grid(row=3, column=0)

# embedded frame to hold card images
playerCardFrame = tkinter.Frame(cardFrame, background="green")
playerCardFrame.grid(row=2, column=1, sticky='ew', rowspan=2)

buttonFrame = tkinter.Frame(mainWindow)
buttonFrame.grid(row=3, column=0, columnspan=3, sticky='w')

dealerButton = tkinter.Button(buttonFrame, text="Stay", command=dealDealer)
dealerButton.grid(row=0, column=0)

playerButton = tkinter.Button(buttonFrame, text="Hit", command=dealPlayer)
playerButton.grid(row=0, column=1)

newGameButton = tkinter.Button(buttonFrame, text="New Game", command=newGame)
newGameButton.grid(row=0, column=2)

shuffleButton = tkinter.Button(buttonFrame, text="shuffle", command=shuffle)
shuffleButton.grid(row=0, column=3)

# load cards
cards = []
loadImages(cards)
print(cards)

# create a new deck and shuffle
deck = list(cards + list(cards) + list(cards))
shuffle()
# Create list to store dealer and players hands
dealerHand = []
playerHand = []

if __name__ == '__main__':
    play()
