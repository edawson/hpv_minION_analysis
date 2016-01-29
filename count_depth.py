"""This script takes in GAM-JSON and counts
the number of edits at a given position. This
is a pseduo-measure of read-depth / depth for a
given event at a specific site. We expect that
low counts at a site indicate a randomly-introduced
error, while high depth hopefully represents a true
variant.

Eric T Dawson, inspired by Erik Garrison
January 2016"""

import json
import sys

def make_edit(edit):
    for p in edit:
        try:
            p["from_length"]
            from_length = int(p["from_length"])
        except KeyError:
            from_length = 0;
        try:
            seq = p["sequence"]
        except KeyError:
            seq = ""
        try:
            to_length = int(p["to_length"])
        except KeyError:
            to_length = 0
    return from_length, to_length, seq

def make_pos(pos):
    try:
        offset = int(pos["offset"])
    except KeyError:
        offset = 0
    try:
        n_id = int(pos["node_id"])
    except KeyError:
        n_id = 0
    return n_id, offset


if __name__ == "__main__":

    edit_to_count = {}

    infile = sys.argv[1]
    with open(infile, "r") as ifi:
        for line in ifi:
            jj = json.loads(line)
            path = jj["path"]
            mapping = path["mapping"]
            for i in xrange(0,len(mapping)):
                #print mapping[i]
                e = make_edit(mapping[i]["edit"])
                p = make_pos(mapping[i]["position"])
                ## Use <node_id>_<offset> as the dictionary key,
                ## as it's the closest analogue to a base number.
                pos_hash = "_".join([str(p[0]), str(p[1])])
                if pos_hash in edit_to_count:
                    edit_to_count[pos_hash] += 1
                else:
                    edit_to_count[pos_hash] = 1

            for i in edit_to_count:
                print i, edit_to_count[i]


                #if mapping[i]["edit"] in edit_to_count:
                #    edit_to_count["".join(mapping[i]["edit"])] += 1
                #else:
                #    edit_to_count[mapping[i]["edit"]] = 1
