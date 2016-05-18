#!/usr/bin/python
from __future__ import print_function
from collections import defaultdict
from subprocess import call
import argparse
import sys
import os

vg = "~/sandbox/hpv_minION_analysis/vg/bin/vg"
msga_args = "-t 4 -K 16 -B 256 -GS .75 -C"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", dest="infile", required=True, type=str, help="The preclustered output of Mash")
    parser.add_argument("-d", "--distance", dest="dist", required=False, type=float, default=0.1, help="Maximum allowed distance for a strain to be considered a relative of another strain.")
    parser.add_argument("-p", "--path", dest="outpath", required=False, type=str, default="./", help="A custom path to store MSGA graphs in.")

    return parser.parse_args()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def make_fastas(neighbors):
    s = ""
    for i in neighbors:
        s += ("-f" + " " + i + " ")
    return s

def make_outfile_name(neighbors):
    s = "msga"
    for i in neighbors:
        s += ("_" + os.path.basename(i))
    s += ".vg"
    
    return s


def run_msga(neighbors):
    run_str = vg + " " + "msga" + " " + msga_args
    fastas = make_fastas(neighbors)
    outfile = make_outfile_name(neighbors);
    
    run_str = run_str + " " + fastas + " " + ">" + " " + outfile

    call(run_str, shell=True)
    #ret = run_str
    #return ret

if __name__ == "__main__":
    args = parse_args()

    eprint("running")     


    strain_to_neighbors = defaultdict(list)

    with open(args.infile, "r") as ifi:
        for line in ifi:
            tokens = line.strip().split("\t")
            if float(tokens[2]) > args.dist:
                continue
            else:
                strain_to_neighbors[tokens[1]].append(tokens[0])

    #ret = defaultdict(int)

    for i in strain_to_neighbors.keys():
        if len(strain_to_neighbors[i]) is 0:
                continue
        else:
            run_msga(strain_to_neighbors[i])

        for j in strain_to_neighbors[i]:
            #print (i, j)
            if j in strain_to_neighbors:
                del strain_to_neighbors[j]
