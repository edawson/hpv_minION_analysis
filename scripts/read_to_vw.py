import sys

g_key_to_label = {}

class Rec:
    def __init__(self):
        self.iden = ""
        self.seq = ""
        self.label = 0
    
    def to_str(self):
        return "%s 1.0 \'%s | vectorspace %s" % (self.label, self.iden, self.seq)

if __name__ == "__main__":
    count = 0
    rec = None
    for line in sys.stdin:
        if line.starts_with(">"):
            if line.strip() in g_key_to_label:
                if rec is not None:
                    print rec.to_str()
                rec = Rec()
                rec.label = g_key_to_label
                rec.iden = "_".join([line.strip().split(" ")])
            elif line.starts_with("A") or line.starts_with("C") or line.startswith("T") or line.startswith("G"):
                rec.seq += line.strip()
