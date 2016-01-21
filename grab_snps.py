import sys
import datetime
import re
def make_vcf(line):
    ret = []
    ## Break the line into tokens and strip them of whitespace
    splits = [x.strip() for x in line.strip().split(",")]
    
    ## Grab only relevant fields and convert to string
    fields = [1, 6, 7, 8]
    ret.append("HPV16Ref")
    ret.append(splits[18])
    ret.append(".")

    patt = re.compile("[ACTG]*")
    cond = patt.match
    ret.append(splits[6] if len(cond(splits[6]).group()) > 0 else "")
    ret.append(splits[7] if len(cond(splits[7]).group()) > 0 else "")
    ret.append("40")
    ret.append("PASS")
    #if "hom" in splits[8].lower():
    #    splits[8] = "./."

    vcf_line = "\t".join(ret)  #.join([splits[i] for i in fields])
    return vcf_line

def make_header(out_list, file_name):
    header = "##fileFormat=VCFv4.1\n"
    now = datetime.datetime.now()
    header += "##fileDate=" + now.strftime("%d%m%Y") + "\n"
    header += "##source=" + str(file_name) + "\n"
    #header += "##\n"
    header += "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER"
    
    return header

def valid(line):
    patt = re.compile("[0-9]*")
    dna_patt = re.compile("[ACTG]*")
    if len(patt.match((line.split(",")[18])).group()) > 0: # and \
    #len(dna_patt.match((line.split(",")[6])).group()) > 0 and \
    # len(dna_patt.match((line.split(",")[7])).group()) > 0:
        return True
    else:
        return False

def sort_by_pos(out_list):
    ret = []
    d = {}
    for i in out_list:
        k = i.split("\t")[1]
        d[k] = i
    
    for i in sorted(d):
        ret[i] = d[i]
    
    return ret

if __name__ == "__main__":
    out_list = []
    with open(sys.argv[1], "r") as fi:
        for line in fi:
            if (valid(line)):
                out_list.append(make_vcf(line))
    d = {}
    for i in out_list:
        k = int(i.split("\t")[1])
        d[k] = i

    print make_header(out_list, sys.argv[1])
    for i in sorted(d):
        print d[i]

