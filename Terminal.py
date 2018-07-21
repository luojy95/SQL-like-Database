from optparse import OptionParser
import sys
from myCSV import *
from index_management import buildTreeForSingleAttr
import ntpath
from SQLparse import Sql_parsing


def main():
    parser = OptionParser()
    # Define option to read csv files
    parser.add_option("-f", "--filepath", action="store", type="string", dest="filepath", default=None)
    # Define option to set path for index files
    parser.add_option("-p", "--indexpath", action="store", type="string", dest="indexpath", default=None)
    (options, args) = parser.parse_args()
    # Decide how many csv files the program need to read
    if options.filepath is not None:
        CSVfile = []
        CSVfile.append(options.filepath)
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
    # Show different options
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
            Attribs= ind.split(" ")
            filepath = Attribs[0]
            filename = ntpath.basename(filepath)
            AttrId = getAttrID(filepath, Attribs[1])
            if AttrId < 0:
                print("Fail to build index")
            else:
                if Attribs[2] == 'y':
                    buildTreeForSingleAttr(filename, filepath, options.indexpath, AttrId, return_tree=False, isNumber=True)
                else:
                    buildTreeForSingleAttr(filename, filepath, options.indexpath, AttrId, return_tree=False, isNumber=False)
                print("Index for " + Attribs[1] + " build successfully")
        elif selection == 2:
            sql = input("Input SQL Command:\n")
            S = Sql_parsing(sql, options.indexpath)
        elif selection == 3:
            print("Exit!")
            break
        else:
            print("invalid choice")

if __name__ == "__main__":
    main()