from optparse import OptionParser
import sys
from myCSV import *
from index_management import buildTreeForSingleAttr
import ntpath
from SQLparse import Sql_parsing
from split import my_seperater
from select_and_print import PairCsvandAlias
import time
import json

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
        CSV_split = {}
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
                CSV_split[f] = 1
            except:
                print("Fail to read the file")
                sys.exit(0)
    else:
        print("No csv files to read")
        sys.exit(0)
    # Show different options
    while True:
        selectionString = "\nChoose an option:\n" \
                          "\t1.	Preprocess\n" \
                          "\t2.	Read in total\n" \
                          "\t3.	Build index\n" \
                          "\t4.	Run Query\n" \
                          "\t5.	Exit\n"
        try:
            selection = int(input(selectionString))
        except:
            selection = 0
        if selection == 1:
            limit = int(input("Input the split limit:\n"))
            print('Preprocessing...')
            for f in CSVfile:
                if countRowNumber(f) > limit:
                    split_num = my_seperater(limit,f)
                    CSV_split[f] = split_num
                else:
                    CSV_split[f] = 1
                json.dump(CSV_split, open('CSV_split', 'w'))
        elif selection == 2:
            for f in CSVfile:
                CSV_split[f] = 1
            json.dump(CSV_split, open('CSV_split', 'w'))
        elif selection == 3:
            # Build Btrees for the input attribute
            CSV_split = json.load(open('CSV_split'))
            ind = input("Build index for:\n")
            Attribs= ind.split(" ")
            filepath = Attribs[0]
            filename = ntpath.basename(filepath)
            AttrId = getAttrID(filepath, Attribs[1])
            if AttrId < 0:
                print("Fail to build index")
            else:
                if Attribs[2] == 'y':
                    if CSV_split[filename] ==1:
                        buildTreeForSingleAttr(filename, filepath, options.indexpath, AttrId, return_tree=False,
                                               isNumber=True)
                    else:
                        for i in range(CSV_split[filename]):
                            f = filename.split('.')[0] + '_split_' + str(i) + '.csv'
                            fp = f
                            buildTreeForSingleAttr(f, fp, options.indexpath, AttrId, return_tree=False,
                                                   isNumber=True)
                else:
                    if CSV_split[filename] ==1:
                        buildTreeForSingleAttr(filename, filepath, options.indexpath, AttrId, return_tree=False,
                                               isNumber=False)
                    else:
                        for i in range(CSV_split[filename]):
                            f = filename.split('.')[0] + '_split_' + str(i) + '.csv'
                            fp = f
                            buildTreeForSingleAttr(f, fp, options.indexpath, AttrId, return_tree=False,
                                                   isNumber=False)
                print("Index for " + Attribs[1] + " build successfully")
        elif selection == 4:
            # Execute Query
            sql = input("Input SQL Command:\n")
            sqlist =splitSQL(sql, CSV_split)
            fin_result = []
            start = time.time()
            attrlist = []
            for q in sqlist:
                attr, result = Sql_parsing(q, options.indexpath).get_result()
                if attr == []:
                    pass
                else:
                    attrlist = attr
                fin_result = fin_result + result
            query_time = time.time() - start
            print("---------------------the result of query is as followed:-----------------------")
            print(attrlist)
            for row in fin_result:
                print(row)
            print('There are '+ str(len(fin_result)) + ' records found in total!')
            print('Finish Query in ' + str(query_time) + ' seconds')
        elif selection == 5:
            print("Exit!")
            break
        else:
            print("invalid choice")

def splitSQL(sql, CSV_split):
    sqlist = [sql]
    csv_used, alias_colume = PairCsvandAlias(sql)
    for j in range(len(csv_used)):
        sqlist_new = []
        if CSV_split[csv_used[j]] > 1:
            for q in sqlist:
                for i in range(CSV_split[csv_used[j]]):
                    q_new = q.replace(csv_used[j]+' '+alias_colume[j], csv_used[j].split('.')[0]
                                      + '_split_' + str(i) + '.csv '+ alias_colume[j])
                    sqlist_new.append(q_new)
            sqlist = sqlist_new
        else:
            pass
    return sqlist

if __name__ == "__main__":
    main()