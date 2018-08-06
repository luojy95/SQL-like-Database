
from BTrees.OOBTree import OOBTree
import os
import sys
from myCSV import *
import _pickle as cPickle
# import ubjson
import gzip


def buildTreeForAttr(dictAttr, fileName, attrIndx, file_path, return_tree):
    """
    This funciton accepts a dctionary dictAttr, build an OOBtree, store the value in OOBTree and then
    dump the Btree object into a file with name defined as fileName + _Attr_ + attrIndx + _.tree
    Args:
        dictAttr: a dictionary that store the (attribute, row index set) pair
        fileName: csvfile name without '.csv'
        attrIndx: index of attribute
        file_path: path to store the btree file
    Returns:
        None
    """
    sys.setrecursionlimit(100000)
    t = OOBTree()
    t.update(dictAttr)
    os.makedirs(file_path, exist_ok=True)
    with open(file_path + '/' + fileName + '_Attr_' + str(attrIndx) + '_.tree', "wb") as f:
        cPickle.dump(t, f)
    if return_tree:
        return t
    # with gzip.open(file_path + fileName + '_Attr_' + str(attrIndx) + '_.tree', "wb") as f:
    #     ubjson.dump(t, f)

def recoverFromPickle(BtreefileName, file_path):
    """
    This funciton accepts a BtreefileName stored in the file_path and return a btree object
    Args:
        BtreefileName: '.tree' file that store the btree file
        file_path: path to store the btree file
    Returns:
        btree: object that use attribute value as key, row index set as value
    """
    with open(file_path + BtreefileName, 'rb') as f:
        btree = cPickle.load(f, encoding='bytes')
        return btree
    # with gzip.open(file_path + BtreefileName, 'rb') as f:
    #     btree = ubjson.load(f)
    #     return btree

def recoverFromPickle2(Btreefilepath):
    """
    This funciton accepts a BtreefileName stored in the file_path and return a btree object
    Args:
        Btreefilepath: path to '.tree' file that store the btree file
    Returns:
        btree: object that use attribute value as key, row index set as value
    """
    with open(Btreefilepath, 'rb') as f:
        btree = cPickle.load(f, encoding='bytes')
        return btree
    # with gzip.open(file_path + BtreefileName, 'rb') as f:
    #     btree = ubjson.load(f)
    #     return btree
