import csv
from myCSV import *
from mybtree import *
# import gzip
import time
from select_and_print import *

import operator



from join import *
    
def buildTreeForSingleAttr(fileName, dataFilePath, BtreeFilePath, AttrId, return_tree, isNumber):
    '''
    build Btrees for one attribute, with fileName (without .csv suffix) and store it in the file_path
    return the tree if return_tree is true
    Args:
         isNumber: if the attribute is a number
         AttrId: the index of column that is considered as the key in file fileName
         return_tree: if the tree will be returned
         dataFilePath: path of data file
         BtreeFilePath: path of btree file
    Returns:
         Bt: a btree stores the (value of attr, offset) as the key-value pair
    '''
    AttrDict = buildDictForAttr(dataFilePath, AttrId, isNumber)#build attribute dictionary
    FName = fileName.split('.')[0]#file name without csv suffix
    Bt = buildTreeForAttr(AttrDict, FName, AttrId, BtreeFilePath, return_tree)
    if return_tree:
        return Bt


def buildDictForAttr(filePath, attrIndx, isNumber):
    """
    This funciton returns a dictionary that store the set of offset for all tuples
        that share the same value for attribute of index attrIndx
    Args:
        fileName
        attrIndx: the index of column that is considered as the key in file fileName
        isNumber: if the attribute is a number
    Returns:
        dict_attr: key = attribute with index attrIndx for each tuple , Note: Index 0 is the title.
                   value = a list of integers indicate the offset in file
    """
    dict_attr = {}
    with open(filePath, 'rb') as f:   
        reader = csv.reader(f)
        dict_attr = {}
        f.seek(0)
        offset = 0
        offset_list = []
        for line in f:
            offset += len(line)
            offset_list.append(offset)
        f.seek(0)
    with open(filePath, 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f)
        row_ID = 0
        # iterate through each row
        for rd in reader:
            if row_ID == 0:#skip title
                row_ID += 1
                continue
            if isNumber:
                try:
                    key = float(rd[attrIndx])
                except:
                    key = 0.0
            else:
                key = rd[attrIndx].upper()
            if key in dict_attr:
                #append row index w.r.t the tuple to the list
                dict_attr[key].append(offset_list[row_ID - 1])
            else:
                #create a list that store the row index w.r.t the tuple
                dict_attr[key] = [offset_list[row_ID - 1]]
            row_ID += 1
        return dict_attr















