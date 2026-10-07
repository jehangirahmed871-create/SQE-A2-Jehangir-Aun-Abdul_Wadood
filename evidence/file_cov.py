import sys
info = sys.argv[1]
targets = sys.argv[2:]
cur = None
d = {}
for raw in open(info):
    raw = raw.strip()
    if raw.startswith('SF:'):
        cur = None
        for t in targets:
            if raw.endswith('/' + t):
                cur = t
                d[cur] = {'LF': 0, 'LH': 0, 'BRF': 0, 'BRH': 0}
    elif cur and raw.split(':')[0] in ('LF', 'LH', 'BRF', 'BRH'):
        k, v = raw.split(':')
        d[cur][k] = int(v)
for t in targets:
    c = d.get(t)
    if not c:
        print(t, "not found")
        continue
    print("%-28s lines %3d/%3d (%.1f%%)  branches %3d/%3d (%.1f%%)" % (
        t, c['LH'], c['LF'], 100.0 * c['LH'] / max(c['LF'], 1),
        c['BRH'], c['BRF'], 100.0 * c['BRH'] / max(c['BRF'], 1)))
