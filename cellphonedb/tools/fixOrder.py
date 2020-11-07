#!/usr/bin/python
import sys
import csv
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

if len(sys.argv) != 2:
    print("Usage: python {} ccout/means.txt")
    sys.exit()

with open(sys.argv[1]) as f:
    f_tsv = csv.reader(f, delimiter = "\t")
    headers = next(f_tsv)
    print("\t".join(headers))
    idx = 11 if headers[11] != "rank" else 12
    headori = headers[0:idx]
    for i in headers[idx:]:
        cts = i.split("|")
        i_rev = "|".join(cts[::-1])
        headori.append(i_rev)
    idm = [headori.index(x) for x in headers[idx:]]
    for row in f_tsv:
        [rec_a, rec_b] = row[7:9]
        if rec_a == "True" and rec_b == "False":
            row[2:9] = [row[x] for x in [3,2,5,4,6,8,7]]
            row[idx:] = [row[x] for x in idm]
        out = "\t".join(row)
        sys.stdout.write(out + "\n")
