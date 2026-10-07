import re, sys
src_name = sys.argv[1]
cur = None
src = {}
stats = {}
for raw in open(src_name + '.gcov', errors='replace'):
    raw = raw.rstrip('\n')
    m = re.match(r'^\s*([^:]+):\s*(\d+):(.*)$', raw)
    if m:
        ln = int(m.group(2))
        if ln > 0:
            cur = ln
            src[ln] = m.group(3).strip()
        continue
    if raw.startswith('branch') and cur:
        missed = ('never executed' in raw) or re.search(r'taken 0\b', raw)
        thr = '(throw)' in raw
        d = stats.setdefault(cur, [0, 0, 0, 0])   # total, missed_throw, missed_other, total_throw
        d[0] += 1
        d[3] += 1 if thr else 0
        if missed:
            if thr:
                d[1] += 1
            else:
                d[2] += 1
tot = sum(d[0] for d in stats.values())
mt = sum(d[1] for d in stats.values())
mo = sum(d[2] for d in stats.values())
tt = sum(d[3] for d in stats.values())
print("branches total=%d  of which exception edges=%d" % (tot, tt))
print("missed: exception edges=%d  other=%d" % (mt, mo))
if tt == 0:
    print("NOTE: no '(throw)' annotations found in gcov output")
print("\nlines with missed NON-exception branches:")
for ln in sorted(stats):
    if stats[ln][2] > 0:
        print("%4d | missed=%d | %s" % (ln, stats[ln][2], src[ln][:90]))
