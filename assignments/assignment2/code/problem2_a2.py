

class Conga:

    def __init__(self):
        self.board = [
            ['b 10', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', 'w 10'],
        ]
        self.white_turn = False

    def generate_moves(self):
        pass

    def is_white(self, c):
        if 'w' in self.board[c[0]][c[1]]:
            return True
        return False

    def is_black(self, c):
        if 'b' in self.board[c[0]][c[1]]:
            return True
        return False




conga = Conga()
print(conga.board)
print(conga.is_white((3, 3)))