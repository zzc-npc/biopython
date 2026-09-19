from rna_toolkit.commands.stats import _n50, _median, _gc_content


# ---------- N50 ----------

def test_n50_empty():
    assert _n50([]) == 0


def test_n50_one():
    assert _n50([100]) == 100


def test_n50_classic():
    # 总长 300，一半 150
    # 100 → 100
    #  80 → 180 ≥ 150  → N50 = 80
    assert _n50([100, 80, 60, 40, 20]) == 80


def test_n50_order_independent():
    assert _n50([20, 40, 60, 80, 100]) == 80


def test_n50_two_equal():
    # 总长 100，一半 50
    # 50 → 50 ≥ 50  → N50 = 50
    assert _n50([50, 50]) == 50


# ---------- median ----------

def test_median_empty():
    assert _median([]) == 0


def test_median_odd():
    assert _median([20, 40, 60]) == 40


def test_median_even():
    assert _median([20, 40, 60, 80]) == 50


def test_median_one():
    assert _median([42]) == 42


# ---------- GC ----------

def test_gc_empty():
    assert _gc_content("") == 0.0


def test_gc_all_gc():
    assert _gc_content("GCGC") == 1.0


def test_gc_none():
    assert _gc_content("AUAU") == 0.0


def test_gc_half():
    assert _gc_content("ACGU") == 0.5


def test_gc_n_ignored():
    # N 不算 GC，也不算总长？算总长，只是不计入 GC
    # 序列 ACGUN：G+C=2，总长 5，GC = 2/5 = 0.4
    assert _gc_content("ACGUN") == 0.4
