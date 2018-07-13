import csv
from myCSV import *
from mybtree import *
# import gzip
import time
def buildDictForAttr(filePath, attrIndx):
    """
    This funciton returns a dictionary that store the row index set for all tuples
        that share the same value for attribute of index attrIndx
    Args:
        fileName
        attrIndx: the index of column that is considered as the key in file fileName
    Returns:
        dict_attr: key = attribute with index attrIndx for each tuple , Note: Index 0 is the title.
                   value = a list of integers indicate the row indices
    """
    dict_attr = {}
    with open(filePath, 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f)
        row_ID = 0
        # iterate through each row
        for rd in reader:
            row_ID += 1
            if row_ID == 1:#skip title
                continue
            if rd[attrIndx] in dict_attr:
                #append row index w.r.t the tuple to the list
                dict_attr[rd[attrIndx]].append(row_ID)
            else:
                #create a list that store the row index w.r.t the tuple
                dict_attr[rd[attrIndx]] = [row_ID]
        return dict_attr

def buildTreeForAllAttr(fileName, dataFilePath, BtreeFilePath):
    '''
    build Btrees for all attributes, with fileName (without .csv suffix) and store them in the file_path
    '''
    att_list = (getAttrList(dataFilePath))
    for att in range(len(att_list)):
        dcc = buildDictForAttr(dataFilePath, att)
        FName = fileName.split('.')[0]#file name without csv suffix
        buildTreeForAttr(dcc, FName, att, BtreeFilePath, return_tree = False)

def buildTreeForSingleAttr(fileName, dataFilePath, BtreeFilePath, AttrId, return_tree):
    '''
    build Btrees for one attribute, with fileName (without .csv suffix) and store it in the file_path
    return the tree if return_tree is true
    '''
    AttrDict = buildDictForAttr(dataFilePath, AttrId)#build attribute dictionary
    FName = fileName.split('.')[0]#file name without csv suffix
    Bt = buildTreeForAttr(AttrDict, FName, AttrId, BtreeFilePath, return_tree)
    if return_tree:
        return Bt

def main():
    #a small unit test to check the functionality of index/btree creation
    fileName = 'review-5k.csv'
    dataFilePath = './data/' + fileName
    filepathBtree = './btree/'

    # build btrees for all attributes
    buildTreeForAllAttr(fileName, dataFilePath, filepathBtree)
    btt = buildTreeForSingleAttr(fileName, dataFilePath, filepathBtree, AttrId = 1, return_tree = True)

    print(btt.keys())
    #recover btree from btreeFile
    btreeFile = 'review-5k_Attr_0_.tree'
    btree = recoverFromPickle(btreeFile, filepathBtree)

    # print(list(btree.keys()))
    # print(list(btree.values('2')));
    # for k, it in btree.iteritems():
    #     print(k, it)
    # btree.items();


start = time.time()
main()
print('time = ', time.time() - start)
