from player import Player

from player import Player
from abc import ABCMeta, abstractmethod

FILES = "abcdefgh"
RANKS = "12345678"


class Piece(metaclass=ABCMeta):
    def __init__(self, player, loc):
        if not isinstance(player, Player):
            raise Exception
        self.loc = loc
        self.player = player
        self.relative_moves = []
        self.name_of_piece = ' '
        self.initial_configs()
        self.player_configs()

    @abstractmethod
    def initial_configs(self):
        pass

    def __repr__(self):
        return f"\033[33m{self.name_of_piece}\033[0m"

    def player_configs(self):
        if self.player == Player.WHITE:
            self.name_of_piece = self.name_of_piece.upper()

        elif self.player == Player.BLACK:
            self.name_of_piece = self.name_of_piece.lower()
            self.relative_moves = [(-x, -y) for x, y in self.relative_moves]

    def _possible_move(self, stop):
        file_start, rank_start = self.loc
        file_stop, rank_stop = stop

        for r, f in self.relative_moves:
            rank_condition = int(rank_stop) - int(rank_start) == r
            file_condition = ord(file_stop) - ord(file_start) == f
            if rank_condition and file_condition:
                return True

        return False

    def move(self, stop):
        print(self, self.loc, stop)
        if self._possible_move(stop):
            cb = ChessBoard()
            cb[self.loc] = '.'
            cb[stop] = self
            self.loc = stop
            return True

        return False


class Pawn(Piece):
    def initial_configs(self):
        self.name_of_piece = 'P'
        self.relative_moves = [(1, 0), (2, 0)]


class Knight(Piece):
    def initial_configs(self):
        self.name_of_piece = 'N'
        self.relative_moves = [(1, 2), (1, -2), (2, 1), (2, -1),
                               (-1, 2), (-1, -2), (-2, -1), (-2, 1)]


class Bishop(Piece):
    def initial_configs(self):
        self.name_of_piece = 'B'
        self.relative_moves = [(1, 0), (2, 0)]


class Rook(Piece):
    def initial_configs(self):
        self.name_of_piece = 'R'
        self.relative_moves = [(1, 0), (2, 0)]


class Queen(Piece):
    def initial_configs(self):
        self.name_of_piece = 'Q'
        self.relative_moves = [(1, 0), (2, 0)]


class King(Piece):
    def initial_configs(self):
        self.name_of_piece = 'K'
        self.relative_moves = [(1, 0), (2, 0)]



class ChessBoard:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.is_initiated = False

        return cls._instance

    def __init__(self):
        if not self.is_initiated:
            self.is_initiated = True

            self.turn = Player.WHITE
            self.__chess_board = {rank: {file: '.' for file in FILES} for rank in RANKS}
            self.__chess_board['2'] = {file: Pawn(Player.WHITE, f"{file}2") for file in FILES}
            self.__chess_board['7'] = {file: Pawn(Player.BLACK, f"{file}7") for file in FILES}
            self.__chess_board['1'] = {
                'a': Rook(Player.WHITE, 'a1'),
                'b': Knight(Player.WHITE, 'b1'),
                'c': Bishop(Player.WHITE, 'c1'),
                'd': Queen(Player.WHITE, 'd1'),
                'e': King(Player.WHITE, 'e1'),
                'f': Bishop(Player.WHITE, 'f1'),
                'g': Knight(Player.WHITE, 'g1'),
                'h': Rook(Player.WHITE, 'h1')
            }
            self.__chess_board['8'] = {
                'a': Rook(Player.BLACK, 'a8'),
                'b': Knight(Player.BLACK, 'b8'),
                'c': Bishop(Player.BLACK, 'c8'),
                'd': Queen(Player.BLACK, 'd8'),
                'e': King(Player.BLACK, 'e8'),
                'f': Bishop(Player.BLACK, 'f8'),
                'g': Knight(Player.BLACK, 'g8'),
                'h': Rook(Player.BLACK, 'h8')
            }

    def __repr__(self):
        text = ""
        for rank in self.__chess_board:
            line = " ".join(map(str, self.__chess_board[rank].values()))

            text = f"\033[31;1m{rank:<2}\033[0m{line}\n{text}"

        text += "  \033[32;2ma b c d e f g h\033[0m"
        return text

    def move_piece(self, start, stop):
        if self.turn == Player.BLACK and self[start].name_of_piece.isupper():
            raise Exception

        if self.turn == Player.WHITE and self[start].name_of_piece.islower():
            raise Exception

        # self[stop] = self[start]
        # self[start] = "."
        self[start].move(stop)
        self.turn = Player.BLACK if self.turn == Player.WHITE else Player.WHITE

    def __getitem__(self, loc: str):
        file, rank = loc
        return self.__chess_board[rank][file]

    def __setitem__(self, loc, value):
        file, rank = loc
        self.__chess_board[rank][file] = value


chess_board = ChessBoard()
chess_board.move_piece("e2", "e4")
chess_board.move_piece("c7", "c5")
chess_board.move_piece("g1", "f3")
chess_board.move_piece("d7", "d5")

print(chess_board)