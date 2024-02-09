from DAVEcore import ElasticCatenary

def test_zerowidth_pointcount():
    """An elastic catenary with zero width should have 3 points, regardless of the number of requested samples."""
    p1 = [0, 0, 0]
    p2 = [0, 0, 1]
    cat = ElasticCatenary(*p1, *p2, 1000, 2, 0.5)
    pts = cat.GetPoints(100)
    #
    # import matplotlib.pyplot as plt
    # plt.plot([p[0] for p in pts], [p[2] for p in pts])
    # plt.show()


    assert len(pts) == 3