import random

# Example card: {"number": "K", "suite": "clubs"}

"""
Globals: What are the available numbers and suites
Jacks of the given suites are excluded in this list but will be added in the deck
Spade and hearts have single eyed jacks, clubs and diamonds have two eyes
"""
available_numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
available_suites = ["hearts", "diamonds", "spades", "clubs"]

class Square:
    """
    Implements the functionality of a square
    Each square should know:
        - what is the number and suite assigned to it
        - what is the status: color of the chip present in the square or empty
        - if a chip is present is it removable
    """
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
        return "[{} of {}, {}]".format(self.card["number"], self.card["suite"], self.status)

class Board:
    """
    Captures the state of board
    """
    def __init__(self, size = 5, seq_len = 4, seq_count = 1):
        """
        Initializes a board of given size. Size 5 implies board of 5x5
        Currently works only for odd numbers (One wild in the center).
        To Do: Add support for even numbers (Corner wilds)
        """
        self.size = size
        self.seq_len = seq_len
        self.seq_count = seq_count
        self.board = [[None for i in range(self.size)] for j in range(self.size)]
        self.lookup = {}
        i = 0
        j = 0
        for _ in range(2):
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
                    key = card["number"] + "_" + card["suite"]
                    if key in self.lookup.keys():
                        self.lookup[key].append((i, j))
                    else:
                        self.lookup[key] = []
                        self.lookup[key].append((i, j))
                    j += 1
                    if j == size:
                        i += 1
                        j = 0

    def check_sequence(self, color):
        # Check rows
        count = 0
        for row in range(self.size):
            streak = 0
            for j in range(self.size):
                if self.get_status(row, j) == color:
                    streak += 1
                    if streak == self.seq_len:
                        streak = 0
                        count += 1
                        if count == self.seq_count:
                            return True
        # Check cols
        for col in range(self.size):
            streak = 0
            for i in range(self.size):
                if self.get_status(i, col) == color:
                    streak += 1
                    if streak == self.seq_len:
                        streak = 0
                        count += 1
                        if count == self.seq_count:
                            return True

        for s in range(2*self.size - 1):
            streak = 0
            for i in range(s + 1):
                j = s - i
                if i < self.size and j < self.size:
                    if self.get_status(i, j) == color:
                        streak += 1
                        if streak == self.seq_len:
                            streak = 0
                            count += 1
                            if count == self.seq_count:
                                return True

        for d in range(-1*self.size + 1, self.size):
            streak = 0
            for j in range(0, 2*self.size - 1):
                i = j + d
                if i >= 0 and i < self.size and j < self.size:
                   if self.get_status(i, j) == color:
                       streak += 1
                       if streak == self.seq_len:
                           streak = 0
                           count += 1
                           if count == self.seq_count:
                               return True

        return False

    def check_terminal(self):
        check_sequence("red")
        check_sequence("blue")

    def get_status(self, i, j):
        return self.board[i][j].status

    def is_removable(self, i, j):
        return self.board[i][j].isRemovable

    def place_chip(self, i, j, color):
        self.board[i][j].place_chip(color)

    def remove_chip(self, i, j):
        self.board[i][j].remove_chip()

    def get_empty_squares(self):
        """
        Return a list of coordinates empty squares on the board
        """
        empty_squares = []
        for i in range(self.size):
            for j in range(self.size):
                if self.get_status(i, j) == "empty":
                    empty_squares.append((i, j))
        return empty_squares

    def get_squares_by_chip_color(self, color):
        """
        Takes in an argument color and returns the list of coordinates of squares occupied by that color
        """
        color_squares = []
        for i in range(self.size):
            for j in range(self.size):
                if self.get_status(i, j) == color:
                    color_squares.append((i, j))
        return color_squares

    def __repr__(self):
        """ 
        Utility Function to print board
        To Do: Make this beautiful
        """
        board_str = ""
        for i in range(self.size):
            for j in range(self.size):
                board_str += str(self.board[i][j])
                board_str += " "
            board_str += "\n"
        return board_str

class Deck:
    """
    Captures the state of the deck
    """
    def __init__(self):
        self._deck = []
        for s in available_suites:
            for n in available_numbers:
                card = {}
                card["number"] = n
                card["suite"] = s
                self._deck.append(card)
                self._deck.append(card)
            card = {}
            card["number"] = "J"
            card["suite"] = s
            self._deck.append(card)
        random.shuffle(self._deck)

    def draw(self):
        return self._deck.pop()

class Player:
    def __init__(self, color):
        self.color = color
        self._cards = []

    def draw(self, deck):
        self._cards.append(deck.draw())

    def show_cards(self):
        print(self._cards)

    def available_moves(self, board):
        """
        Move can be characterized by card and location
        """
        moves = []
        for i in range(len(self._cards)):
            card = self._cards[i]
            if card["number"] != "J":
                key = card["number"] + "_" + card["suite"]
                locs = board.lookup[key]
                for loc in locs:
                    if board.get_status(loc[0], loc[1]) == "empty":
                        moves.append((i, loc))
            else:
                if card["suite"] == "spades" or card["suite"] == "hearts": # Single eyed jacks
                    if self.color == "red":
                        opp_color = "blue"
                    else:
                        opp_color = "red"
                    locs = board.get_squares_by_chip_color(opp_color)
                    for loc in locs:
                        if board.is_removable(loc[0], loc[1]) == True:
                            moves.append((i, loc))
                else: # Double eyed jacks
                    locs = board.get_empty_squares()
                    for loc in locs:
                        moves.append((i, loc))
        return moves

    def play(self, move, board, deck):
        card = self._cards.pop(move[0])
        loc = move[1]
        i = loc[0]
        j = loc[1]
        if card["number"] == "J" and (card["suite"] == "spades" or card["suite"] == "hearts"):
            board.remove_chip(i, j)
        else:
            board.place_chip(i, j, self.color)
        if board.check_sequence(self.color):
            return "win"
        try:
            self.draw(deck)
        except:
            return "draw"
        return "continue"

    def random_play(self, board, deck):
        moves = self.available_moves(board)
        if len(moves) == 0:
            return "draw"
        reco_move = random.choice(moves)
        return self.play(reco_move, board, deck)

def test():
    board = Board(5, 4, 1)
    deck = Deck()
    print(len(deck._deck))
    for i in range(3):
        print(deck.draw())
    print(len(deck._deck))
    p1 = Player("red")
    p2 = Player("blue")
    p1.draw(deck)
    p2.draw(deck)
    p1.draw(deck)
    p2.draw(deck)
    p1.show_cards()
    p2.show_cards()
    print(len(deck._deck))
    moves = p1.available_moves(board)
    print(moves[0])
    p1.play(moves[0], board, deck)
    print(board)
    print(board.check_sequence("red"))

def simulate(size, seq_len, num_seq):
    board = Board(size, seq_len, num_seq)
    deck = Deck()
    p1 = Player("red")
    p2 = Player("blue")
    p1.draw(deck)
    p2.draw(deck)
    p1.draw(deck)
    p2.draw(deck)
    p1.draw(deck)
    p2.draw(deck)
    turn = 0
    p1_win = False
    p2_win = False
    while True:
        print(board)
        if turn == 0:
            result = p1.random_play(board, deck)
            if result == "win":
                return 1
            elif result == "draw":
                return 0
            turn = 1
        else:
            result = p2.random_play(board, deck)
            if result == "win":
                return -1
            elif result == "draw":
                return 0
            turn = 0

def main():
    # test()
    win = 0
    loss = 0
    draw = 0
    for _ in range(1000):
        r = simulate(9, 5, 2)
        if r == 1:
            win += 1
        elif r == 0:
            draw += 1
        else:
            loss += 1
    print("win/loss/draw: {}/{}/{}".format(win, loss, draw))

if __name__ == "__main__":
    main()
