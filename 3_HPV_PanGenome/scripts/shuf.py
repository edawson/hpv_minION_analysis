#!/usr/bin/python
import sys
import argparse
import random


class FQRecord:
    def __init__(self):
        self.seq = ""
        self.qual = ""
        self.anno = ""
        self.name = ""

    def string(self):
        ret = "@" + self.name.strip() + "\n" + \
        self.seq + "\n" + \
        "+" + self.anno + "\n" + \
        self.qual
        return ret


"""Takes in a pseudo fasta and makes a
pseudo fastq from it"""
def make_fastq(record, name, fake_qual, seq="", anno=""):
    if record.name == "":
        record.name = name
    
    record.qual = "".join([fake_qual for i in xrange(0, len(record.seq))])

    return record

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="infile", type=str, required=True)
    parser.add_argument("-n", dest="namebase", type=str, required=True)
    parser.add_argument("-q", dest="qual", type=str, required=True)
    return parser.parse_args()
    

if __name__ == "__main__":
    ## Add the sample name to the front of the
    ## read line.
    rec_list = []
    count = 0
    record = None
    for line in sys.stdin:
        count += 1
        if count == 1:
            record = FQRecord()
            record.name = line.strip().strip("@")
        elif count == 2:
            record.seq = line.strip()
        elif count == 3:
            record.anno = line.strip().strip("+")
        elif count == 4:
            record.qual = line.strip()
            rec_list.append(record)
            count = 0

    random.shuffle(rec_list)

    for i in rec_list:
        print i.string()
