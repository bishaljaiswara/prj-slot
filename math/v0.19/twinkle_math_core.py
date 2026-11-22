"""Twinkle Treats v0.19 standalone rules core.

This is a deterministic rules implementation/test harness, NOT Stake Engine SDK code.
All wallet-facing amounts are integer hundredths of the original bet.
"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

ROWS, COLS = 5, 6
MIN_CLUSTER = 5
WILD = "wild"
BONUS = "bonus"
SYMBOL_ORDER = ("gem", "berry", "blue", "lolli", "orange", "heart", "lemon")
PAY_PER_SYMBOL = {
    "gem": Decimal("0.05528"), "berry": Decimal("0.06219"),
    "blue": Decimal("0.0691"), "lolli": Decimal("0.093285"),
    "orange": Decimal("0.10365"), "heart": Decimal("0.13129"),
    "lemon": Decimal("0.17275"),
}
MAX_CASCADES = 12
MAX_CASCADE_MULTIPLIER = Decimal("4.0")
CASCADE_STEP = Decimal("0.25")
MAX_FREE_SPINS = 500
MAX_ROUND_HUNDREDTHS = 2_500_000


def to_hundredths(multiplier: Decimal | str | int | float) -> int:
    """Round an individual component to nearest 0.01x, ROUND_HALF_UP."""
    value = Decimal(str(multiplier)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int(value * 100)


@dataclass(frozen=True)
class Cluster:
    symbol: str
    cells: tuple[int, ...]

    @property
    def size(self) -> int:
        return len(self.cells)


def _neighbors(index: int) -> Iterable[int]:
    r, c = divmod(index, COLS)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if 0 <= rr < ROWS and 0 <= cc < COLS:
                yield rr * COLS + cc


def find_clusters(board: list[str]) -> list[Cluster]:
    """Find eligible 8-way clusters and greedily resolve overlaps deterministically."""
    if len(board) != ROWS * COLS:
        raise ValueError(f"board must contain exactly {ROWS * COLS} cells")
    if any(s not in (*SYMBOL_ORDER, WILD, BONUS) for s in board):
        raise ValueError("board contains an unknown symbol")

    candidates: list[Cluster] = []
    for symbol in SYMBOL_ORDER:
        eligible = {i for i, s in enumerate(board) if s == symbol or s == WILD}
        seen: set[int] = set()
        for start in sorted(eligible):
            if start in seen:
                continue
            stack, component = [start], []
            seen.add(start)
            while stack:
                cur = stack.pop()
                component.append(cur)
                for nxt in _neighbors(cur):
                    if nxt in eligible and nxt not in seen:
                        seen.add(nxt)
                        stack.append(nxt)
            if len(component) >= MIN_CLUSTER and any(board[i] == symbol for i in component):
                candidates.append(Cluster(symbol, tuple(sorted(component))))

    priority = {s: i for i, s in enumerate(SYMBOL_ORDER)}
    candidates.sort(key=lambda x: (-x.size, priority[x.symbol], x.cells[0]))
    claimed: set[int] = set()
    accepted: list[Cluster] = []
    for candidate in candidates:
        if claimed.isdisjoint(candidate.cells):
            accepted.append(candidate)
            claimed.update(candidate.cells)
    return accepted


def cluster_component_hundredths(cluster: Cluster, cascade_multiplier: Decimal) -> int:
    raw = PAY_PER_SYMBOL[cluster.symbol] * cluster.size * cascade_multiplier
    return to_hundredths(raw)


@dataclass
class PaidRoundWallet:
    credited_hundredths: int = 0

    @property
    def remaining_hundredths(self) -> int:
        return MAX_ROUND_HUNDREDTHS - self.credited_hundredths

    def credit_component(self, component_hundredths: int) -> int:
        if component_hundredths < 0:
            raise ValueError("negative payouts are forbidden")
        credited = min(component_hundredths, self.remaining_hundredths)
        self.credited_hundredths += credited
        return credited

    def credit_multiplier(self, multiplier: Decimal | str | int | float) -> int:
        return self.credit_component(to_hundredths(multiplier))


def scatter_award(scatter_count: int) -> tuple[int, bool]:
    """Return (free spins, hidden feature trigger) for one spin sequence."""
    if scatter_count < 3:
        return 0, False
    if scatter_count == 3:
        return 5, False
    if scatter_count == 4:
        return 10, False
    return 15, True


def clamp_retrigger(current_total: int, newly_awarded: int) -> int:
    if current_total < 0 or newly_awarded < 0:
        raise ValueError("free-spin counts cannot be negative")
    return min(newly_awarded, max(0, MAX_FREE_SPINS - current_total))


def next_cascade_multiplier(current: Decimal) -> Decimal:
    return min(MAX_CASCADE_MULTIPLIER, current + CASCADE_STEP)
