import sys

if __name__ == "__main__":
    with open(sys.argv[1], "r") as fi:
        for line in fi:
            if "a" in line or "g" in line:
                print line.upper().strip()
            else:
                print line.strip()
