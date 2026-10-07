import sys
cur = None
files = []
for line in open('coverage/lcov_filtered.info'):
    line = line.strip()
    if line.startswith('SF:'):
        cur = {'f': line[3:], 'LF': 0, 'LH': 0, 'BRF': 0, 'BRH': 0}
    elif line.startswith(('LF:', 'LH:', 'BRF:', 'BRH:')):
        k, v = line.split(':')
        cur[k] = int(v)
    elif line == 'end_of_record':
        files.append(cur)

filt = sys.argv[1] if len(sys.argv) > 1 else ''
rows = []
for c in files:
    p = c['f']
    i = p.find('src/')
    if i < 0:
        continue
    p = p[i:]
    if not p.endswith('.cpp'):
        continue
    if 'test' in p.lower():
        continue
    if not (p.startswith('src/modules') or p.startswith('src/lib')):
        continue
    if filt and filt not in p:
        continue
    if c['LF'] < 60 or c['BRF'] < 30:
        continue
    lp = 100.0 * c['LH'] / c['LF']
    bp = 100.0 * c['BRH'] / c['BRF']
    if bp >= 100:
        continue
    rows.append((p, c['LF'], lp, c['BRF'], bp, c['BRF'] - c['BRH']))

rows.sort(key=lambda r: -r[5])
print("%-62s %5s %6s %5s %6s %7s" % ("file", "LF", "line%", "BRF", "br%", "br_miss"))
for r in rows[:int(sys.argv[2]) if len(sys.argv) > 2 else 40]:
    print("%-62s %5d %6.1f %5d %6.1f %7d" % r)
