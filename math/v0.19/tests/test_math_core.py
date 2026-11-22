from decimal import Decimal
import pytest
from twinkle_math_core import (
    PaidRoundWallet, clamp_retrigger, find_clusters,
    next_cascade_multiplier, scatter_award, to_hundredths,
)


def board_with(cells, fill="bonus"):
    b = [fill] * 30
    for i, s in cells.items():
        b[i] = s
    return b


def test_eight_way_cluster_and_wild_substitution():
    b = board_with({0:"gem", 7:"gem", 14:"gem", 21:"gem", 28:"wild"})
    clusters = find_clusters(b)
    assert len(clusters) == 1
    assert clusters[0].symbol == "gem"
    assert clusters[0].size == 5


def test_wild_only_does_not_pay():
    assert find_clusters(["wild"] * 30) == []


def test_no_cell_is_paid_twice_when_candidates_overlap():
    b = board_with({0:"gem", 1:"gem", 2:"gem", 3:"gem", 4:"wild",
                    5:"berry", 11:"berry", 17:"berry", 23:"berry"})
    got = find_clusters(b)
    claimed = [i for c in got for i in c.cells]
    assert len(claimed) == len(set(claimed))


def test_board_size_validation():
    with pytest.raises(ValueError):
        find_clusters(["gem"] * 29)


@pytest.mark.parametrize("value,expected", [("1.005",101),("1.004",100),("0.005",1)])
def test_round_half_up(value, expected):
    assert to_hundredths(value) == expected


def test_round_cap_clips_last_component():
    w = PaidRoundWallet(credited_hundredths=2_499_980)
    assert w.credit_multiplier("10.00") == 20
    assert w.credited_hundredths == 2_500_000
    assert w.credit_multiplier("1.00") == 0


@pytest.mark.parametrize("n,fs,hidden", [(2,0,False),(3,5,False),(4,10,False),(5,15,True),(8,15,True)])
def test_scatter_tiers(n, fs, hidden):
    assert scatter_award(n) == (fs, hidden)


def test_free_spin_ceiling():
    assert clamp_retrigger(498, 10) == 2
    assert clamp_retrigger(500, 10) == 0


def test_cascade_multiplier_ceiling():
    assert next_cascade_multiplier(Decimal("3.75")) == Decimal("4.00")
    assert next_cascade_multiplier(Decimal("4.00")) == Decimal("4.00")
