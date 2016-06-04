import sys
from subprocess import call

class frec:
    def __init__(self):
        self.name = ""
        self.seq = ""
        self.qual = ""
        self.anno = ""

    def stringify(self):
        return "\n".join([self.name, self.seq, self.anno, self.seq])

if __name__ == "__main__":

    sketch = "HPV_pan.sketch3000_k10.msh"

    f_dict = {}
    rec = None
    for line in sys.stdin:
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
    for rec in f_dict:
        with open("tmp.txt", "w") as ofi:
            ofi.write(f_dict[rec].stringify())
        run_str = "../bin/mash dist " + sketch + " tmp.txt  | sort -n -k3 | head -n 1 > " + str(count) + "_seq.txt"
        call(run_str, shell=True)
        count += 1
