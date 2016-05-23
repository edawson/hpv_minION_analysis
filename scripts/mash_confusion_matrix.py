import sys
import argparse
from collections import defaultdict
from make_confusion_matrix import make_matrix
from make_confusion_matrix import mat_to_string


g_label_to_class = {}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", dest="infile", type=str, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    
    args = parse_args()

    with open(args.infile, "r") as ifi:
        for line in ifi:
            tokens = line.strip().split()
            key = ".".join(tokens[0].split(".")[0:2])
            if key not in g_label_to_class:
                g_label_to_class[key] = defaultdict(int)
            call = ".".join(tokens[1].split(".")[0:2])
            g_label_to_class[key][call] += 1


        
    print mat_to_string(g_label_to_class)


