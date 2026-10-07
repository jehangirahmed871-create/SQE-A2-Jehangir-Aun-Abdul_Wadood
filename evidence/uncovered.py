import sys, os

target = sys.argv[1]

# Locate the real source file under src/
src_path = None
for root, dirs, files in os.walk('src'):
    if target in files and 'manual_control' in root:
        src_path = os.path.join(root, target)
        break
if not src_path:
    print("Source file not found for", target)
    sys.exit(1)
src = open(src_path).read().split('\n')

cur = False
lines, brs = set(), {}
for raw in open(sys.argv[2] if len(sys.argv) > 2 else 'coverage/lcov_filtered.info'):
    raw = raw.strip()
    if raw.startswith('SF:'):
        cur = raw[3:].endswith('/' + target) or raw[3:] == target
    elif cur and raw.startswith('DA:'):
        ln, cnt = raw[3:].split(',')[:2]
        if int(cnt) == 0:
            lines.add(int(ln))
    elif cur and raw.startswith('BRDA:'):
        ln, blk, br, taken = raw[5:].split(',')
        if taken in ('-', '0'):
            brs[int(ln)] = brs.get(int(ln), 0) + 1

def text(n):
    return src[n - 1].strip()[:100] if 0 < n <= len(src) else ''

print("FILE:", src_path)
print("\n== UNCOVERED LINES (%d) ==" % len(lines))
for n in sorted(lines):
    print("%4d | %s" % (n, text(n)))
print("\n== LINES WITH MISSED BRANCHES (%d lines) ==" % len(brs))
for n in sorted(brs):
    print("%4d | missed=%d | %s" % (n, brs[n], text(n)))
