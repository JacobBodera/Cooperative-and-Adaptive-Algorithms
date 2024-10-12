import copy
import math


class CongaGame:
    def __init__(self):
        self.BLACK = "B"
        self.WHITE = "W"
        self.board = [[None for _ in range(4)] for _ in range(4)]
        self.stones = [[0 for _ in range(4)] for _ in range(4)]
        self.board[0][0], self.board[3][3] = self.BLACK, self.WHITE
        self.stones[0][0], self.stones[3][3] = 10, 10
        self.current_player = self.BLACK

    def display_board(self):
        print("")
        for i in range(len(self.board)):
            line = ""
            for j in range(len(self.board[0])):
                if self.board[i][j] is None:
                    line += " - "
                else:
                    line += " " + str(self.board[i][j]) + " "
            line += "   "
            for j in range(len(self.stones[0])):
                line += " " + str(self.stones[i][j]) + " "
            print(line)
        print("")

    def generate_moves(self, board, player):
        directions = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
        moves = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] is None or board[i][j] != player:
                    continue
                for d in directions:
                    m = (i, j, d)
                    if self.is_legal_move(i, j, d):
                        moves.append(m)
        return moves

    def is_legal_move(self, r, c, d):
        r = r + d[0]
        c = c + d[1]
        if 0 <= r < 4 and 0 <= c < 4 and (self.board[r][c] is None or self.board[r][c] == self.current_player):
            return True
        return False

    def evaluate(self, board):
        return len(self.generate_moves(board, self.WHITE)) - len(self.generate_moves(board, self.BLACK))

    def opposite(self, player):
        return self.BLACK if player == self.WHITE else self.WHITE

    def switch_player(self):
        self.current_player = self.opposite(self.current_player)

    def make_move(self, board, stones, move):
        r, c, dr, dc = move[0], move[1], move[2][0], move[2][1]
        moving_player = board[r][c]
        stone_count = stones[r][c]
        stones[r][c] = 0

        new_r = r + dr
        new_c = c + dc

        while 0 <= new_r < 4 and 0 <= new_c < 4 and board[new_r][new_c] is not self.opposite(moving_player) and stone_count > 0:
            stones[new_r][new_c] += 1
            stone_count -= 1
            board[new_r][new_c] = moving_player

            new_r = new_r + dr
            new_c = new_c + dc

        stones[new_r - dr][new_c - dc] += stone_count
        board[r][c] = None
        return board

    def is_game_over(self, board):
        if len(self.generate_moves(board, self.BLACK)) == 0 or len(self.generate_moves(board, self.BLACK)) == 0:
            return True
        return False

    def minmax_alpha_beta(self, board, stones, depth, maximizing_player, alpha = -math.inf, beta = math.inf):
        if depth == 0 or self.is_game_over(board):
            return self.evaluate(board), None

        best_move = None

        if not maximizing_player:
            max_eval = math.inf
            for move in self.generate_moves(board, self.BLACK):
                new_board = self.make_move(board, stones, move)
                eval, _ = self.minmax_alpha_beta(new_board, stones, depth - 1, True, alpha, beta)
                if eval < max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = -math.inf
            for move in self.generate_moves(board, self.WHITE):
                new_board = self.make_move(board, stones, move)
                eval, _ = self.minmax_alpha_beta(new_board, stones, depth - 1, False, alpha, beta)
                if eval > min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move



def convert_dir(dir):
    if dir == "N":
        return (-1, 0)
    elif dir == "S":
        return (1, 0)
    elif dir == "E":
        return (0, 1)
    elif dir == "W":
        return (0, -1)
    elif dir == "NE":
        return (-1, 1)
    elif dir == "NW":
        return (-1, -1)
    elif dir == "SE":
        return (1, 1)
    elif dir == "SW":
        return (1, -1)

def play_conga_manual():
    game = CongaGame()
    safety_count = 0
    game.display_board()
    while not game.is_game_over(game.board) and safety_count < 500:
        if game.current_player == game.BLACK:
            print("BLACKS TURN")
            r = int(input("Enter row: "))
            c = int(input("Enter column: "))
            d = input("Enter direction: ")
            d = convert_dir(d)
            game.make_move(game.board, game.stones, (r, c, d))
        if game.current_player == game.WHITE:
            print("WHITES TURN")
            r = int(input("Enter row: "))
            c = int(input("Enter column: "))
            d = input("Enter direction: ")
            d = convert_dir(d)
            game.make_move(game.board, game.stones, (r, c, d))

        game.switch_player()
        game.display_board()
        safety_count += 1

def play_conga():
    game = CongaGame()
    safety_count = 0
    game.display_board()
    while not game.is_game_over(game.board) and safety_count < 500:
        if game.current_player == game.BLACK:
            e, move = game.minmax_alpha_beta(copy.deepcopy(game.board), copy.deepcopy(game.stones), depth = 5, maximizing_player = False)
            print(f"Best move: {move}, Eval: {e}")
            game.make_move(game.board, game.stones, move)
        if game.current_player == game.WHITE:
            e, move = game.minmax_alpha_beta(copy.deepcopy(game.board), copy.deepcopy(game.stones), depth = 5, maximizing_player = True)
            print(f"Best move: {move}, Eval: {e}")
            r = int(input("Enter row: "))
            c = int(input("Enter column: "))
            d = input("Enter direction: ")
            d = convert_dir(d)
            game.make_move(game.board, game.stones, (r, c, d))
        print("---------------------------")

        game.switch_player()
        game.display_board()
        safety_count += 1

play_conga()






