import sys

def coverage_filter(line, min_cov=0.5):
    line_len = float(len(line.split("\t")) - 1.0)
    zero_count = len([x for x in line.split("\t")[1:] if "0" in x])
    if ((line_len - float(zero_count)) / line_len) >= min_cov:
        return line
    else:
        return ""

if __name__ == "__main__":
    with open(sys.argv[1], "r") as fi:
        for line in fi:
            fil = coverage_filter(line, 0.7)
            if fil is not "":
                print fil
            else:
                continue

