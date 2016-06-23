import sys
import argparse
from collections import defaultdict
from make_confusion_matrix import make_matrix
from make_confusion_matrix import mat_to_string
from make_confusion_matrix import mat_to_tidy


g_label_to_class = {}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", dest="infile", type=str, required=True)
    parser.add_argument("-c", "--classes", dest="classfile", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    
    args = parse_args()

    numkey_to_class = {}                                                                                                                                                                                                                                 
    if args.classfile is not None:
        with open(args.classfile, "r") as cfi:
            for line in cfi:
                tokens = line.strip().split("\t")
                numkey_to_class[tokens[0]] = tokens[1]

    mat = make_matrix({numkey_to_class[i]: {} for i in numkey_to_class})

    with open(args.infile, "r") as ifi:
        for line in ifi:
            tokens = line.strip().split(",")
            #key = ".".join(tokens[0].split(".")[0:2])
            key = tokens[0]
            if key not in g_label_to_class:
                g_label_to_class[key] = defaultdict(int)
            #call = ".".join(tokens[1].split(".")[0:2])
            call = tokens[1]
            g_label_to_class[key][call] += 1
    for i in g_label_to_class:
        for j in g_label_to_class:
            mat[i][j] = g_label_to_class[i][j]


        
    print mat_to_tidy(mat)


