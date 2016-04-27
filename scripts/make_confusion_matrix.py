#!/usr/bin/python
import sys




if __name__ == "__main__":
    count_dict = {}
    for line in sys.stdin:
        splits = line.strip().split(" ")
        label = splits[1]
        pred = splits[0]
        if label not in count_dict:
            count_dict[label] = {}
        if pred not in count_dict[label]:
            count_dict[label][pred] = 0
        count_dict[label][pred] += 1

    for i in count_dict:
        for j in count_dict[i]:
            for k in count_dict:
                if j not in count_dict[k]:
                    count_dict[k][j] = 0

    # A simple header
    #print "\t", "\t".join([i for i in count_dict])

    for i in count_dict:
        outstr = ""
        for j in count_dict[i]:
            outstr += "\t" + str(count_dict[i][j]) + "\t"
        print outstr
