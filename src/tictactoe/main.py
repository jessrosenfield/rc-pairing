#!/usr/bin/env python

from functools import cached_property

BOARD_SIZE = 3
LINE = "".join(["-"] * (2 * BOARD_SIZE - 1))
DELIM = f"\n{LINE}\n"


def generate_win_conditions() -> set[tuple[int]]:
    wins = []
    for i in range(BOARD_SIZE):
        # horizontal win
        start = i * BOARD_SIZE
        wins.append(tuple(range(i * BOARD_SIZE, (i + 1) * BOARD_SIZE)))

        # vertical win
        start = i
        wins.append(tuple(range(i, BOARD_SIZE ** 2, BOARD_SIZE)))

    # left diag
    start = 0
    wins.append(tuple(range(0, BOARD_SIZE ** 2, BOARD_SIZE + 1)))

    # right diag
    wins.append(tuple(range(BOARD_SIZE - 1, BOARD_SIZE ** 2 - 1, BOARD_SIZE - 1)))

    return set(wins)

WIN_CONDITIONS = generate_win_conditions()



class Board:
    def __init__(self):
        self.x = set()
        self.y = set()

    def to_list(self) -> list[str]:
        board = [" "] * BOARD_SIZE**2
        for move in self.x:
            board[move] = "X"
        for move in self.y:
            board[move] = "Y"
        return board

    def get_legal_moves(self) -> set[int]:
        moves = set()
        for i in range(BOARD_SIZE ** 2):
            if i not in self.x and i not in self.y:
                moves.add(i)
        return moves


def pprint_board(board: Board, hint=False):
    items = board.to_list()
    if hint:
        items = [item if item != " " else i for i, item in enumerate(items)]
    rows = []
    for i in range(BOARD_SIZE):
        row = board[i * BOARD_SIZE : i * BOARD_SIZE + BOARD_SIZE]
        rows.append("|".join(row))
    print(DELIM.join(rows))


class TicTacToe:
    def __init__(self):
        self.__x_turn = True
        self.board = Board()
    
    @property
    def current_player(self) -> str:
        if self.__x_turn:
            return "X"
        return "Y"

    def toggle_player(self):
        self.__x_turn = not self.__x_turn

    def is_active(self):
        return self.winner is None and len(self.x) + len(self.y) < BOARD_SIZE ** 2

    @cached_property
    def winner(self):
        items = self.board.to_list()
        for win in WIN_CONDITIONS:
            if items[win[0]] == items[win[1]] == items[win[2]] != " ":
                return items[win[0]]
        return None
    
    def play(self, position: int):
        if self.winner:
            raise ValueError(f"Cannot apply move to finished game. Winner: {self.winner}")

        if position not in self.get_legal_moves():
            raise ValueError(f"Illegal move: {position}")

        if self.current_player == "X":
            self.x.add(position)
        else:
            self.y.add(position)

        del self.winner
        self.toggle_player()


def get_next_move(board: Board) -> int:
    while True:
        legal_moves = board.get_legal_moves()
        raw_position = input("Enter your next move: ")
        try:
            position = int(raw_position)
            if position in legal_moves:
                return position
        except ValueError:
            print(f"Invalid position. Try again with one of the available moves: {sorted(legal_moves)}")
            pprint(game.to_board(), hint=True)
            print("\n")
    

def main():
    game = TicTacToe()
    while game.is_active():
        print(f"{game.current_player}'s turn")
        get_next_move(game.board)
        print()
    print(f"WINNER: {game.winner}")
    pprint(game.to_board())


if __name__ == "__main__":
    main()