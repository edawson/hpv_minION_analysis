import sys
import argparse
from collections import defaultdict

global_type_to_count = defaultdict(int)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--classes", type=str, dest="classfile", required=False, default=None, help="A file with the number-to-class translations, one per line")
    parser.add_argument("-i", "--infile", type=str, dest="infile", required=False, default=None, help="A tab-delimited prediction file with predictions in the first column and labels in the second, one entry per row.")
    parser.add_argument("-n", "--no-keys", action='store_true', dest="noKeys", default=False)
    parser.add_argument("-t", "--tidy", action='store_true', dest="tidy", default=False)
    return parser.parse_args()

def make_matrix(class_d):
    ret_d = {}

    keys = class_d.keys();
    for i in keys:
        if i not in ret_d:
            ret_d[i] = {}
        for j in keys:
            ret_d[i][j] = 0

    return ret_d

def mat_to_string(mat, printKeys=True, useComma=True):
    ordered_keys = sorted(mat.keys())

    sep = "\t" if not useComma else ","
    ostr = ""

    
    if printKeys:
        #ostr = "Actual" + sep
        #ostr = sep
        ostr = ""
        # Header time:
        ostr += sep.join(ordered_keys) + "\n"

    for key_one in ordered_keys:
        if printKeys:
            ostr += key_one + sep
        count = 0
        for key_two in ordered_keys:
            ostr += str(mat[key_one][key_two])
            if count < len(ordered_keys) - 1:
                ostr += sep
        ostr += "\n"
    return ostr

def mat_to_tidy(mat):
    ordered_keys = sorted(mat.keys())
    # Format:
    # Actual Call
    # HPV16 HPV1

    ostr = ""
    for key_one in ordered_keys:
        for key_two in ordered_keys:
            ostr += str(key_one) + "," + str(key_two) + "," + str(mat[key_one][key_two]) + "\n"

    return ostr

if __name__ == "__main__":
    
    args = parse_args()
    
    numkey_to_class = {}
    if args.classfile is not None:
        with open(args.classfile, "r") as cfi:
            for line in cfi:
                tokens = line.strip().split("\t")
                numkey_to_class[tokens[0]] = tokens[1]
    
    mat = make_matrix({numkey_to_class[i]: {} for i in numkey_to_class})

    #print mat['hpv_16'].keys()


    ## VW outputs the label and the class call
    ## All the labels should be pretty much the same / irrelevant
    for line in sys.stdin:
        tokens = line.strip().split()
        if len(numkey_to_class) > 0:
            mat[numkey_to_class[tokens[0]]][tokens[1].strip()] += 1

    printKeys = False if args.noKeys else True
    print mat_to_tidy(mat) if args.tidy else mat_to_string(mat, printKeys)
