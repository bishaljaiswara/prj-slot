"""Twinkle Treats 8-way cluster resolver for the Stake Engine Math SDK port."""
from __future__ import annotations

ROWS, COLS = 5, 6
MIN_CLUSTER = 5
SYMBOL_PRIORITY = ("GEM", "BERRY", "BLUE", "LOLLI", "ORANGE", "HEART", "LEMON")
WILD = "W"

def _neighbours(index: int):
    row, col = divmod(index, COLS)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr, cc = row + dr, col + dc
            if 0 <= rr < ROWS and 0 <= cc < COLS:
                yield rr * COLS + cc

def resolve_clusters(board):
    """Input is row-major 5x6 symbol strings; returns disjoint deterministic clusters."""
    if len(board) != ROWS or any(len(row) != COLS for row in board):
        raise ValueError("Expected a 5x6 row-major board")
    flat = [symbol for row in board for symbol in row]
    allowed = set(SYMBOL_PRIORITY) | {WILD, "S"}
    if any(symbol not in allowed for symbol in flat):
        raise ValueError("Unknown symbol in board")
    candidates = []
    for symbol in SYMBOL_PRIORITY:
        eligible = {i for i, value in enumerate(flat) if value == symbol or value == WILD}
        seen = set()
        for start in sorted(eligible):
            if start in seen:
                continue
            stack, component = [start], []
            seen.add(start)
            while stack:
                current = stack.pop()
                component.append(current)
                for nxt in _neighbours(current):
                    if nxt in eligible and nxt not in seen:
                        seen.add(nxt)
                        stack.append(nxt)
            if len(component) >= MIN_CLUSTER and any(flat[i] == symbol for i in component):
                candidates.append((symbol, tuple(sorted(component))))
    priority = {symbol: index for index, symbol in enumerate(SYMBOL_PRIORITY)}
    candidates.sort(key=lambda item: (-len(item[1]), priority[item[0]], item[1][0]))
    claimed, accepted = set(), []
    for symbol, cells in candidates:
        if claimed.isdisjoint(cells):
            accepted.append((symbol, cells))
            claimed.update(cells)
    return accepted
