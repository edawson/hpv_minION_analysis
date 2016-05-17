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
                tokens = line.strip().split("\t")
                numkey_to_class[tokens[0]] = tokens[1]

    ## VW outputs the label and the class call
    ## All the labels should be pretty much the same / irrelevant
    count = 0
    c_mod = 2

    for line in sys.stdin:
        tokens = line.strip().split()
        if len(numkey_to_class) > 0:
            global_type_to_count[numkey_to_class[tokens[0]]] += 1
            count += 1
        if count % c_mod == 0:
            k_list = global_type_to_count.keys()
            sys.stderr.write("processed: " + str(count) + "\t" + "\t".join(k_list) + "\n")
            sys.stderr.write("\t\t" + "\t".join([(str(global_type_to_count[i]) + "\t") for i in k_list]) + "\n\n")
            c_mod = c_mod * 2


    c_list = global_type_to_count.keys()

    print "Total processed: ", count
    print "\t".join(c_list)
    #print " ".join([global_type_to_count[i] for i in c_list])
    ostr = ""
    for i in c_list:
        ostr += str(global_type_to_count[i]) + "\t"

    print ostr
