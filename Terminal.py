from optparse import OptionParser
import sys
from myCSV import *

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", action="store", type="string", dest="filename", default=None)
    (options, args) = parser.parse_args()
    if options.filename is not None:
        CSVfile = []
        CSVfile.append(options.filename)
        if len(args) > 0:
            for a in args:
                CSVfile.append(a)
        for f in CSVfile:
            try:
                attrlist = getAttrList(f)
                print("--------------------------------------")
                print("Attributes in " + f + ":")
                print("--------------------------------------")
                for attr in attrlist:
                    print(attr)
                print("--------------------------------------\n")
            except:
                print("Fail to read the file")
                sys.exit(0)
    else:
        print("No csv files to read")
        sys.exit(0)
    while True:
        selectionString = "\nChoose an option:\n" \
                              "\t1.	Build index\n" \
                              "\t2.	Run Query\n" \
                              "\t3.	Exit\n"

        try:
            selection = int(input(selectionString))
        except:
            selection = 0
        if selection == 1:
            ind = input("Build index for:\n")
            print("Index for " + ind + " build successfully")
        elif selection == 2:
            sql = input("Input SQL Command:\n")
            print("Running Query " + sql)
        elif selection == 3:
            print("Exit!")
            break
        else:
            print("invalid choice")

if __name__ == "__main__":
    main()