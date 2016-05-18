import sys

if __name__ == "__main__":
        for line in sys.stdin:
            if "^$" in line:
                continue
            elif ">" in line:
                print (line.strip())[0:25]
            else:
                print line
