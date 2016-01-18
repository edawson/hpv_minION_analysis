import sys


def make_vcf(line):
    ## Break the line into tokens and strip them of whitespace
    splits = [x.strip() for x in line.strip().split(",")]
    
    ## Grab only relevant fields and convert to string
    fields = [0, 1, 2, 3, 4, 5]
    vcf_line = "\t".join([splits[i] for i in fields])
    return vcf_line

def make_header(out_list):
    header = "##VCF4.0\n"
    header += "##source=my_prog\n"
    header += "##\n"
    header += "##\n"
    header += "##\n"
    header += "#CHROM\tPOS\tREF\tALT\tQUAL"
    
    return header


if __name__ == "__main__":
    out_list = []
    with open(sys.argv[1], "r") as fi:
        for line in fi:
            out_list.append(make_vcf(line))

    print make_header(out_list)
    for i in out_list:
        print i

