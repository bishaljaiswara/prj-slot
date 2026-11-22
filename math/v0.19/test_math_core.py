from decimal import Decimal
import pytest
from twinkle_math_core import PaidRoundWallet, clamp_retrigger, find_clusters, next_cascade_multiplier, scatter_award, to_hundredths

def board_with(cells):
    b=["bonus"]*30
    for i,s in cells.items(): b[i]=s
    return b

def test_eight_way_wild_cluster():
    c=find_clusters(board_with({0:"gem",7:"gem",14:"gem",21:"gem",28:"wild"}))
    assert len(c)==1 and c[0].size==5

def test_wild_only_no_win():
    assert find_clusters(["wild"]*30)==[]

def test_no_overlapping_paid_cells():
    c=find_clusters(board_with({0:"gem",1:"gem",2:"gem",3:"gem",4:"wild",5:"berry",11:"berry",17:"berry",23:"berry"}))
    cells=[i for x in c for i in x.cells]
    assert len(cells)==len(set(cells))

def test_wrong_board_size():
    with pytest.raises(ValueError): find_clusters(["gem"]*29)

@pytest.mark.parametrize("v,n",[("1.005",101),("1.004",100),("0.005",1)])
def test_rounding(v,n): assert to_hundredths(v)==n

def test_win_cap():
    w=PaidRoundWallet(2_499_980)
    assert w.credit_multiplier("10.00")==20 and w.credit_multiplier("1.00")==0

@pytest.mark.parametrize("s,fs,h",[(2,0,False),(3,5,False),(4,10,False),(5,15,True),(8,15,True)])
def test_scatter(s,fs,h): assert scatter_award(s)==(fs,h)

def test_free_spin_limit():
    assert clamp_retrigger(498,10)==2 and clamp_retrigger(500,10)==0

def test_cascade_limit():
    assert next_cascade_multiplier(Decimal("3.75"))==Decimal("4.00")
