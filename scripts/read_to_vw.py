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
    count = 1
    rec = None
    for line in sys.stdin:
        if line.startswith("@"):
            seqlab = line.strip().strip("@")
            if rec is not None:
                print rec.to_str()
            if seqlab not in g_key_to_label:
                g_key_to_label[seqlab] = count
                count +=1

            rec = Rec()
            rec.label = g_key_to_label[seqlab]
            rec.iden = "_".join(seqlab.split(" "))
    
        elif (line.startswith("A") or \
                    line.startswith("C") or \
                    line.startswith("T") or \
                    line.startswith("G")):
                rec.seq += line.strip()
