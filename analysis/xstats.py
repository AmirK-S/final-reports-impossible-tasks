"""Exact statistics in pure Python (no scipy). Self-tested by `python3 -I analysis/xstats.py`."""
from math import comb, sqrt
import random

Z = 1.959963984540054


def binom_cdf(k, n, p):
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def clopper_pearson(k, n, alpha=0.05):
    """Exact two-sided (1-alpha) interval for a binomial proportion."""
    if n == 0:
        return (0.0, 1.0)
    if k == 0:
        lower = 0.0
    else:
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if 1 - binom_cdf(k - 1, n, mid) < alpha / 2:   # P(X >= k | mid) too small -> mid too low
                lo = mid
            else:
                hi = mid
        lower = (lo + hi) / 2
    if k == n:
        upper = 1.0
    else:
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if binom_cdf(k, n, mid) > alpha / 2:            # P(X <= k | mid) still large -> mid too low
                lo = mid
            else:
                hi = mid
        upper = (lo + hi) / 2
    return (lower, upper)


def binom_le_p(k, n, p0=0.5):
    """One-sided exact p-value for H0: p >= p0 against p < p0."""
    return binom_cdf(k, n, p0)


def binom_ge_p(k, n, p0=0.5):
    """One-sided exact p-value for H0: p <= p0 against p > p0."""
    return 1 - binom_cdf(k - 1, n, p0) if k > 0 else 1.0


def _hyper(x, n1, n2, m):
    return comb(n1, x) * comb(n2, m - x) / comb(n1 + n2, m)


def fisher_two_sided(a, b, c, d):
    n1, n2, m = a + b, c + d, a + c
    po = _hyper(a, n1, n2, m)
    return min(1.0, sum(_hyper(x, n1, n2, m) for x in range(max(0, m - n2), min(n1, m) + 1)
                        if _hyper(x, n1, n2, m) <= po * (1 + 1e-7)))


def wilson(k, n, z=Z):
    if n == 0:
        return (0.0, 1.0)
    p = k / n; den = 1 + z * z / n; c = p + z * z / (2 * n); h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / den, (c + h) / den)


def newcombe(k1, n1, k2, n2, z=Z):
    """Hybrid score interval for p1 - p2."""
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1, z); l2, u2 = wilson(k2, n2, z)
    d = p1 - p2
    return (d - sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2))


def holm(ps):
    m = len(ps); order = sorted(range(m), key=lambda i: ps[i]); adj = [0.0] * m; run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (m - r) * ps[i])); adj[i] = run
    return adj


def strat_perm(strata, n_perm=200000, seed=20261116):
    """strata: {name: (xs_a, xs_b)} lists of 0/1. Statistic: sum over strata of mean(a) - mean(b).
    One-sided p-value for H1: statistic > 0 (a higher than b). Returns (observed statistic, p)."""
    def st(pairs):
        return sum((sum(a) / len(a) if a else 0) - (sum(b) / len(b) if b else 0) for a, b in pairs)
    obs = st(strata.values()); rng = random.Random(seed); hit = 0
    pools = [(list(a) + list(b), len(a)) for a, b in strata.values()]
    for _ in range(n_perm):
        tot = 0.0
        for pool, na in pools:
            x = pool[:]; rng.shuffle(x)
            a, b = x[:na], x[na:]
            tot += (sum(a) / len(a) if a else 0) - (sum(b) / len(b) if b else 0)
        hit += tot >= obs - 1e-12
    return obs, (hit + 1) / (n_perm + 1)


def cohen_kappa(x, y):
    n = len(x); labs = sorted(set(x) | set(y))
    po = sum(a == b for a, b in zip(x, y)) / n
    pe = sum((x.count(l) / n) * (y.count(l) / n) for l in labs)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def kappa_boot(x, y, n_boot=2000, seed=20261116):
    rng = random.Random(seed); n = len(x); ks = []
    for _ in range(n_boot):
        idx = [rng.randrange(n) for _ in range(n)]
        ks.append(cohen_kappa([x[i] for i in idx], [y[i] for i in idx]))
    ks.sort()
    return (ks[int(0.025 * n_boot)], ks[int(0.975 * n_boot) - 1])


def positive_agreement(x, y, pos):
    a = sum(1 for p, q in zip(x, y) if p == pos and q == pos)
    bc = sum(1 for p, q in zip(x, y) if (p == pos) != (q == pos))
    return (2 * a / (2 * a + bc)) if (2 * a + bc) else float("nan"), 2 * a, 2 * a + bc


if __name__ == "__main__":
    lo, hi = clopper_pearson(0, 30)
    assert abs(hi - 0.11570) < 1e-4 and lo == 0.0, hi
    lo, hi = clopper_pearson(28, 29)
    assert abs(lo - 0.82236) < 1e-4, lo
    lo, hi = clopper_pearson(5, 10)
    assert abs(lo - 0.18709) < 1e-4 and abs(hi - 0.81291) < 1e-4
    assert abs(fisher_two_sided(0, 30, 28, 1) - 0.0) < 1e-12
    assert abs(fisher_two_sided(3, 1, 1, 3) - 0.48571) < 1e-4
    assert abs(cohen_kappa(list("aabb"), list("abab")) - 0.0) < 1e-12
    print("xstats selftest ok")
