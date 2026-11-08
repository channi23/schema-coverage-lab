"""Finite verification of research identities, not a JSON Schema validator.
Run: python3 research-checks/check_semantic_model.py
"""
from itertools import product

checks = 0

def check(value):
    global checks
    assert value
    checks += 1

for n in range(1, 5):
    vectors = list(product((0, 1), repeat=n))
    for b in vectors:
        accepted_exactly_one = sum(b) == 1
        exclusive_regions = any(b[i] and not any(b[:i] + b[i+1:]) for i in range(n))
        check(accepted_exactly_one == exclusive_regions)
    for i in range(n):
        for b in vectors:
            if b[i]:
                continue
            c = b[:i] + (1,) + b[i+1:]
            k = sum(b)
            check((all(b) != all(c)) == (k == n - 1))
            check((any(b) != any(c)) == (k == 0))
            check(((sum(b) == 1) != (sum(c) == 1)) == (k in (0, 1)))

# Every Boolean function and every realizable-cell subset up to 3 predicates.
# Compare the definition by ordered pairs with the adjacent-cell formulation.
models = 0
for n in range(1, 4):
    vectors = list(product((0, 1), repeat=n))
    m = len(vectors)
    for values in product((0, 1), repeat=m):
        f = dict(zip(vectors, values))
        for membership in product((0, 1), repeat=m):
            realizable = {b for b, included in zip(vectors, membership) if included}
            for i in range(n):
                by_pairs = any(
                    b[i] != c[i]
                    and all(b[j] == c[j] for j in range(n) if j != i)
                    and f[b] != f[c]
                    for b in realizable for c in realizable
                )
                by_cells = any(
                    b[:i] + (1 - b[i],) + b[i+1:] in realizable
                    and f[b] != f[b[:i] + (1 - b[i],) + b[i+1:]]
                    for b in realizable
                )
                check(by_pairs == by_cells)
            models += 1

check((sum((1, 1, 1)) % 2 == 1) and not (sum((1, 1, 1)) == 1))
print(f'PASS: {checks} finite identity assertions across {models} function/realizability models')
print('Scope: Boolean/set identities only; no JSON Schema conformance or unbounded feasibility proved.')
