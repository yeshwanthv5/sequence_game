card = {"number": "K", "suite": "clubs"}
# Spade and hearts have single eyed jacks, clubs and diamonds have two eyes

available_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Q", "K"]
available_suites = ["hearts", "diamonds"]

class Square:
    def __init__(self, card):
        self.card = card
        self.status = "empty"
        self.isRemovable = True

        if self.card["number"] == "wild":
            self.status = "wild"
            self.isRemovable = False

    def place_chip(self, color):
        if self.status == "empty":
            self.status = color
        else:
            raise ValueError('Trying to place chip on non empty square!')

    def remove_chip(self):
        if self.isRemovable == True:
            self.status = "empty"
        else:
            raise ValueError('Trying to remove chip from a frozen square!')

    def __repr__(self):
        return "{} of {}, {}".format(self.card["number"], self.card["suite"], self.status)

class Sequence:
    def __init__(self, size):
        self.size = size
        self.board = [[None for i in range(self.size)] for j in range(self.size)]
        i = 0
        j = 0
        for n in available_numbers:
            for s in available_suites:
                if i == int(size/2) and j == int(size/2):
                    card = {}
                    card["number"] = "wild"
                    card["suite"] = "wild"
                    self.board[i][j] = Square(card)
                    j += 1
                card = {}
                card["number"] = n
                card["suite"] = s
                self.board[i][j] = Square(card)
                j += 1
                if j == size:
                    i += 1
                    j = 0

    def print_board(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.board[i][j])
            print("\n")

class Deck:
    def __init__(self):
        self.total_cards = len(available_numbers + 1) * len(available_suites)
        self.remaining_cards = self.total_cards
        self.deck = []
        for s in available_suites:
            for n in available_numbers:
                card = {}
                card["number"] = n
                card["suite"] = s
                self.deck.append(card)
            card = {}
            card["number"] = "J"
            card["suite"] = s
            self.deck.append(card)


def main():
    board = Sequence(5)

if __name__ == "__main__":
    main()
