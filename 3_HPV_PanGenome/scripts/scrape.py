from bs4 import BeautifulSoup as beso
import urllib2 as grabber
import requests
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", dest="infile",  required=True, help="A file with the genbank id in the expected column. Check out the data_locations dir for an idea.")
    parser.add_argument("-d", "--dry-run", dest="dry", required=False, default=False, help="Don't download anything, just do a GET from the server and see what will be downloaded.")

    return parser.parse_args()

def parse_output(output):
    tiny_str = output[0:120]
    genbank_id = tiny_str.split("|")[1]
    hpv_id = (tiny_str.split("|")[-1]).split(" ")[1] + ((tiny_str.split("|")[-1]).split(" ")[4]).strip(",") + "_" + (tiny_str.split("|")[-1]).split(" ")[0]
    return (genbank_id, hpv_id, output)

if __name__ == "__main__":
    args = parse_args()
    
    with open(args.infile, "r") as fi:
        for line in fi:
            if not "#" in line:
                try:
                    ## this works for variants:
                    #query = (line.split(" ")[4]).strip()
                    ## This works for refs
                    query = (line.split(" ")[4]).strip()
                    rep = requests.get('http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=' + query  + '&rettype=fasta&retmode=text')
                    cleaned =  parse_output(rep.text)
                    print "Downloading: ", query
                    if not args.dry:
                        with open(cleaned[1] + "." + "gb" + cleaned[0] + ".fa", "w") as ofi:
                            ofi.write(cleaned[2])
                except KeyboardInterrupt:
                    exit(1)
                except:
                    print "Error, download failed: ", line
