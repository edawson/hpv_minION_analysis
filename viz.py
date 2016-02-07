import re
import sys

def trimLabel(line):
    patt = re.compile("[0-9]*:[ATGCN]*")
    mat = patt.search(line)
    if mat:
        new_label = mat.group().split(":")[0]
        if len(mat.group().split(":")[1]) > 1:
            line = re.sub("[0-9]*:[ATGCN]*", new_label, line)
    else:
        line = line
    return line

def changeShape(line):
    line = re.sub("box", "oval", line)
    return line

def addArrowHead(line):
    if "arrowhead" in line:
        line = re.sub("arrowhead=none", "arrowhead=normal", line)
    return line

def move_tips(line):
    line = re.sub("tailport=ne,", "", line)
    line = re.sub("headport=nw,", "", line)
    return line


def colorVars(line):
    patt = re.compile("[0-9]*:[ATGCN]*")
    mat = patt.search(line)
    if mat:
        new_label = mat.group().split(":")[0]
        if len(mat.group().split(":")[1]) <= 5:
            line = re.sub("shape=box,", "shape=box, color=red,", line)
        else:
            line = line
    return line



if __name__ == "__main__":
    box_shape = "oval"
    doTrimLabel = True
    with open(sys.argv[1], "r") as ifi:
        for line in ifi:
            if doTrimLabel:
                line = trimLabel(line)
            #line = colorVars(line)
            line = changeShape(line)
            #line = addArrowHead(line)
            line = move_tips(line)
            print line.strip()
