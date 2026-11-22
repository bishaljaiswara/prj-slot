from cluster_rules import resolve_clusters

def board(cells, fill="S"):
    flat=[fill]*30
    for i,s in cells.items(): flat[i]=s
    return [flat[r*6:(r+1)*6] for r in range(5)]

def test_eight_way_connected_cluster_with_wild():
    out=resolve_clusters(board({0:"GEM",7:"GEM",14:"GEM",21:"GEM",28:"W"}))
    assert len(out)==1 and out[0][0]=="GEM" and len(out[0][1])==5

def test_wild_only_never_pays():
    assert resolve_clusters([["W"]*6 for _ in range(5)])==[]

def test_scatter_does_not_join_cluster():
    assert resolve_clusters(board({0:"GEM",1:"GEM",2:"GEM",3:"GEM",4:"S"}))==[]

def test_clusters_are_disjoint():
    out=resolve_clusters(board({0:"GEM",1:"GEM",2:"GEM",3:"GEM",4:"W",5:"BERRY",11:"BERRY",17:"BERRY",23:"BERRY"}))
    cells=[cell for _,group in out for cell in group]
    assert len(cells)==len(set(cells))

def test_board_shape_validation():
    import pytest
    with pytest.raises(ValueError): resolve_clusters([["GEM"]*6 for _ in range(4)])
