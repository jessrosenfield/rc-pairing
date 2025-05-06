#!/usr/bin/env python
"""A Tic‑Tac‑Toe CLI
"""

from functools import cached_property
from typing import Final, Iterator, Union
from dataclasses import dataclass

BOARD_SIZE: Final = 3
ROW_SEPARATOR = f'\n{"".join(["-"] * (2 * BOARD_SIZE - 1))}\n'


def _generate_win_conditions() -> tuple[tuple[int, int, int], ...]:
    wins = []
    for i in range(BOARD_SIZE):
        # Row win conditions
        wins.append(tuple(range(i * BOARD_SIZE, (i + 1) * BOARD_SIZE)))
        # Col win conditions
        wins.append(tuple(range(i, BOARD_SIZE**2, BOARD_SIZE)))
    # Diagnoal win conditions
    wins.append(tuple(range(0, BOARD_SIZE**2, BOARD_SIZE + 1)))
    wins.append(tuple(range(BOARD_SIZE - 1, BOARD_SIZE**2 - 1, BOARD_SIZE - 1)))
    return tuple(wins)


WIN_CONDITIONS: Final = _generate_win_conditions()


@dataclass(frozen=True)
class Board:
    """Immutable tic tac toe board state
    * `moves_x`/`moves_o` – frozensets of claimed indices.
    * `x_turn` – whose move next.
    * Iterable: `list(pos)` yields nine cells in row‑major order.

    0|1|2
    -----
    3|4|5
    -----
    6|7|8
    """

    moves_x: frozenset[int] = frozenset()
    moves_o: frozenset[int] = frozenset()
    x_turn: bool = True

    def __iter__(self) -> Iterator[str]:
        for idx in range(BOARD_SIZE**2):
            if idx in self.moves_x:
                yield "X"
            elif idx in self.moves_o:
                yield "O"
            else:
                yield " "

    def __len__(self) -> int:
        return BOARD_SIZE**2

    @property
    def current_player(self) -> str:
        return "X" if self.x_turn else "O"

    def legal_moves(self) -> frozenset[int]:
        return frozenset(
            i for i in range(len(self)) if i not in self.moves_x | self.moves_o
        )

    def winner(self) -> Union[str, None]:
        cells = list(self)
        for a, b, c in WIN_CONDITIONS:
            if cells[a] == cells[b] == cells[c] != " ":
                return cells[a]
        return None

    def is_active(self) -> bool:
        return self.winner() is None and bool(self.legal_moves())

    def with_move(self, move: int) -> "Board":
        if move not in self.legal_moves():
            raise ValueError(f"Illegal move {move}")
        if self.x_turn:
            return Board(self.moves_x | {move}, self.moves_o, x_turn=False)
        return Board(self.moves_x, self.moves_o | {move}, x_turn=True)


class TicTacToe:
    def __init__(self):
        self.board = Board()
        self.moves = 0

    def render(self, show_idx: bool = False) -> str:
        cells = list(self.board)
        if show_idx:
            cells = [v if v != " " else str(i) for i, v in enumerate(cells)]
        rows = [
            "|".join(cells[i : i + BOARD_SIZE])
            for i in range(0, len(cells), BOARD_SIZE)
        ]
        return ROW_SEPARATOR.join(rows)

    def choose_next_move(self) -> int:
        while True:
            try:
                raw = input(
                    f"{self.board.current_player} move {sorted(self.board.legal_moves())}: "
                )
                move = int(raw)
                if move in self.board.legal_moves():
                    return move
            except ValueError:
                pass
            print("Invalid move, try again.")

    def play(self):
        while self.board.is_active():
            print(self.render(show_idx=self.moves == 0))
            print("\n")
            move = self.choose_next_move()
            self.board = self.board.with_move(move)
            self.moves += 1
            print("\n")

        print(self.render())
        print(
            f"\n🏆 Winner: {self.board.winner()}"
            if self.board.winner()
            else "\n🤝 Draw"
        )
        return self.board.winner()


def main():
    TicTacToe().play()


if __name__ == "__main__":
    main()
