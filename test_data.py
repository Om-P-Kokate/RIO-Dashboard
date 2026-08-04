"""Self-check: data.py matches the headline figures asserted in the source HTML."""
import data as D


def test():
    # Counts stated in the HTML's own captions / KPI cards.
    assert len(D.P) == 44, len(D.P)
    assert sum(len(p[4]) for p in D.P) == 56          # "56 route assignments"
    assert sum(a[1] for a in D.ALUM) == 152           # "152 coded records"
    assert sum(D.JOBS.values()) == 293                # "293 job cards"
    assert sum(D.PAT.values()) == 450                 # "450 patent records"
    assert len(D.TERMS) == 10 and len(D.O) == 8 and len(D.DIMS) == 6
    assert len(D.FM) == 7 and len(D.W) == 9 and len(D.SC) == 4

    # "$4.80M awarded · $5.22M proposed" — routes plus the unclassified row.
    awarded = sum(v[0] for v in D.FUND.values()) + D.FUND_UNCLASSIFIED[0]
    proposed = sum(v[1] for v in D.FUND.values()) + D.FUND_UNCLASSIFIED[1]
    assert round(awarded / 1e6, 2) == 4.80, awarded
    assert round(proposed / 1e6, 2) == 5.22, proposed

    # Every route key resolves across every per-route array.
    for k in D.O:
        for arr in (D.ERA, D.FRP, D.SCH, D.FUND, D.ALUMR, D.R):
            assert k in arr, (k, arr)
        assert len(D.R[k]["s"]) == 6
        assert all(1 <= v <= 5 for v in D.R[k]["s"])

    # Scenario route references are valid keys.
    for s in D.SC:
        assert all(k in D.O for k in s["r"]), s

    # No un-decoded HTML entities in the extracted data (the module docstring
    # mentions "&amp;" while describing the decoding, so exclude it).
    blob = repr({k: v for k, v in vars(D).items() if not k.startswith("__")})
    assert "&amp;" not in blob and "&#" not in blob

    # The five unit names that carried entities decoded correctly.
    units = {p[1] for p in D.P}
    assert "Chemical & Biological Engineering" in units
    assert "Electrical, Computer & Energy Engineering" in units
    assert "Civil, Environmental & Architectural Engineering" in units
    assert "Advertising, PR & Media Design" in units
    assert "Speech, Language & Hearing Sciences" in units

    print("ok")


if __name__ == "__main__":
    test()
