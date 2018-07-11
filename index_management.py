import csv
from myCSV import *
from mybtree import *
import gzip
import time
def buildDictForAttr(fileName, attrIndx):
    """
    This funciton return a dictionary that store the row index set for all tuples
        that share the same value for attribute of index attrIndx
    Args:
        fileName
        attrIndx: the index of column that is considered as the key in file fileName
    Returns:
        dict_attr: key = attribute with index attrIndx for each tuple ,
                   value = a list of integers indicate the row indices
    """
    dict_attr = {}
    with open(fileName, 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f)
        row_ID = 0
        # iterate through each row
        for rd in reader:
            row_ID += 1
            if rd[attrIndx] in dict_attr:
                #append row index w.r.t the tuple to the list
                dict_attr[rd[attrIndx]].append(row_ID)
            else:
                #create a list that store the row index w.r.t the tuple
                dict_attr[rd[attrIndx]] = [row_ID]
        return dict_attr

def buildTreeForAllAttr(fileName, file_path):
    '''
    build Btrees for all attributes, with fileName (without .csv suffix) and store them in the file_path
    '''
    att_list = (getAttrList(fileName))
    for att in range(len(att_list)):
        dcc = buildDictForAttr(fileName, att)
        buildTreeForAttr(dcc, fileName.split('.')[0], att, file_path)


def main():
    #a small unit test to check the functionality of index/btree creation
    fileName = 'photos_1w.csv'
    filepathBtree = './btree/'

    # build btrees for all attributes
    buildTreeForAllAttr(fileName, filepathBtree)

    #recover btree from btreeFile
    btreeFile = 'photos_1w_Attr_0_.tree'
    btree = recoverFromPickle(btreeFile, filepathBtree)

    count = 0
    for k, it in btree.items():
        print(k, it)

start = time.time()
main()
print(time.time() - start)
