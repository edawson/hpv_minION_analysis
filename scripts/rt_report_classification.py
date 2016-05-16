import sys
import argparse
from collections import defaultdict

global_type_to_count = defaultdict(int)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--classes", type=str, dest="classfile", required=False, default=None, help="A file with the number-to-class translations, one per line")
    return parser.parse_args()

if __name__ == "__main__":
    
    args = parse_args()
    
    numkey_to_class = {}
    if args.classfile is not None:
        with open(args.classfile, "r") as cfi:
            for line in cfi:
                tokens = line.strip().split(":")
                numkey_to_class[tokens[0]] = tokens[1]

    ## VW outputs the label and the class call
    ## All the labels should be pretty much the same / irrelevant
    for line in sys.stdin:
        tokens = line.strip().split()
        if len(numkey_to_class) > 0:
            global_type_to_count[tokens[0]] += 1

    c_list = global_type_to_count.keys()
    print " ".join(c_list)

    ostr = ""
    for i in c_list:
        ostr += str(global_type_to_count[i]) + " "

    print ostr
