import sys
from subprocess import call
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sketch", dest="sketch", required=True)
    parser.add_argument("-r", "--reads", dest="reads", required=True)

    return parser.parse_args()

class frec:
    def __init__(self):
        self.name = ""
        self.seq = ""
        self.qual = ""
        self.anno = ""

    def stringify(self):
        return "\n".join([self.name, self.seq, self.anno, self.seq])

if __name__ == "__main__":
    args = parse_args()


    sketch = args.sketch

    f_dict = {}
    rec = None
    with open(args.reads, "r") as ifi:
        for line in ifi:
            if line.startswith("@"):
                rec = frec()
                rec.name = line.strip()
            elif line.startswith("+"):
                rec.anno = line.strip()
            elif line.startswith("A") or line.startswith("G") or line.startswith("T") or line.startswith("C"):
                rec.seq = line.strip()
            else:
                rec.qual = line.strip()
                f_dict[rec.name] = rec

    
    count = 0

    with open("mashed.pred.txt", "w") as mfi:
        for rec in f_dict:
            with open(rec.strip("@") + ".tmp", "w") as ofi:
                ofi.write(f_dict[rec].stringify())
            run_str = "../bin/mash dist -i " + sketch + " " + rec.strip("@") + ".tmp | sort -n -k3 | head -n 1 "
            call(run_str, shell=True)
            count += 1
            if count % 10 == 0:
                sys.stderr.write("processed %i reads" % count)
