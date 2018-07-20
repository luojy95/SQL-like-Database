import csv
from myCSV import *
from mybtree import *
# import gzip
import time

import operator



from join import *

# def buildDictForAttr(filePath, attrIndx):
#     """
#     This funciton returns a dictionary that store the row index set for all tuples
#         that share the same value for attribute of index attrIndx
#     Args:
#         fileName
#         attrIndx: the index of column that is considered as the key in file fileName
#     Returns:
#         dict_attr: key = attribute with index attrIndx for each tuple , Note: Index 0 is the title.
#                    value = a list of integers indicate the row indices
#     """
#     dict_attr = {}
#     with open(filePath, 'r', encoding="ISO-8859-1") as f:
#         reader = csv.reader(f)
#         row_ID = 0
#         # iterate through each row
#         for rd in reader:
#             if row_ID == 0:#skip title
#                 row_ID += 1
#                 continue
#             try:
#                 key = float(rd[attrIndx])
#             except:
#                 key = rd[attrIndx]
#
#             if key in dict_attr:
#                 #append row index w.r.t the tuple to the list
#                 dict_attr[key].append(row_ID)
#             else:
#                 #create a list that store the row index w.r.t the tuple
#                 dict_attr[key] = [row_ID]
#             row_ID += 1
#         return dict_attr

# def buildDictForMixedAttr(filePath, attrIndxSet, Operator):
#     """
#     This funciton returns a dictionary that store the row index set for all tuples
#         that share the same value for attribute (which is mixed) of index attrIndx
#     Args:
#         fileName
#         attrIndx: the index of column that is considered as the key in file fileName
#     Returns:
#         dict_attr: key = attribute with index attrIndx for each tuple , Note: Index 0 is the title.
#                    value = a list of integers indicate the row indices
#     """
#     dict_attr = {}
#     ops = { "+": operator.add, "-": operator.sub, '/' : operator.truediv, '*' : operator.mul, '%' : operator.mod} # etc.
#
#     opt_set = ops.keys()
#     for idx in attrIndxSet:
#         try:
#             float(idx)
#             continue
#         except:
#             print('Attributes don\'t support numerical operator')
#             # raise
#
#     with open(filePath, 'r', encoding="ISO-8859-1") as f:
#         reader = csv.reader(f)
#         row_ID = 0
#         # iterate through each row
#         for rd in reader:
#             if row_ID == 0:#skip title
#                 row_ID += 1
#                 continue
#             try:
#                 print(float(rd[attrIndxSet[0]]))
#                 print(float(rd[attrIndxSet[1]]))
#
#             except:
#                 print('Attributes don\'t support numerical operator')
#
#             key = float(ops[Operator](rd[attrIndxSet[0]], rd[attrIndxSet[1]]))
#             if key in dict_attr:
#                 #append row index w.r.t the tuple to the list
#                 dict_attr[key].append(row_ID)
#             else:
#                 #create a list that store the row index w.r.t the tuple
#                 dict_attr[key] = [row_ID]
#             row_ID += 1
#         print(dict_attr[5])
#         return dict_attr

# def buildTreeForAllAttr(fileName, dataFilePath, BtreeFilePath):
#     '''
#     build Btrees for all attributes, with fileName (without .csv suffix) and store them in the file_path
#     '''
#     att_list = (getAttrList(dataFilePath))
#     for att in range(len(att_list)):
#         dcc = buildDictForAttr(dataFilePath, att)
#         FName = fileName.split('.')[0]#file name without csv suffix
#         buildTreeForAttr(dcc, FName, att, BtreeFilePath, return_tree = False)

# def buildTreeForSingleAttr(fileName, dataFilePath, BtreeFilePath, AttrId, return_tree):
#     '''
#     build Btrees for one attribute, with fileName (without .csv suffix) and store it in the file_path
#     return the tree if return_tree is true
#     '''
#     AttrDict = buildDictForAttr(dataFilePath, AttrId)#build attribute dictionary
#     FName = fileName.split('.')[0]#file name without csv suffix
#     Bt = buildTreeForAttr(AttrDict, FName, AttrId, BtreeFilePath, return_tree)
#     if return_tree:
#         return Bt

def buildTreeForMixedAttr(fileName, dataFilePath, BtreeFilePath, attrIndxSet, Operator, return_tree):
    '''
    build Btrees for one attribute, with fileName (without .csv suffix) and store it in the file_path
    return the tree if return_tree is true
    '''
    AttrDict = buildDictForMixedAttr(dataFilePath, attrIndxSet, Operator)#build attribute dictionary
    FName = fileName.split('.')[0]#file name without csv suffix
    AttrId = str(attrIndxSet[0]) + 'x' + str(attrIndxSet[1])
    Bt = buildTreeForAttr(AttrDict, FName, AttrId, BtreeFilePath, return_tree)
    if return_tree:
        return Bt
def buildTreeForSingleAttr(fileName, dataFilePath, BtreeFilePath, AttrId, return_tree, isNumber):
    '''
    build Btrees for one attribute, with fileName (without .csv suffix) and store it in the file_path
    return the tree if return_tree is true
    isNumber: if the attribute is a number
    '''
    AttrDict = buildDictForAttr(dataFilePath, AttrId, isNumber)#build attribute dictionary
    FName = fileName.split('.')[0]#file name without csv suffix
    Bt = buildTreeForAttr(AttrDict, FName, AttrId, BtreeFilePath, return_tree)
    if return_tree:
        return Bt


def buildDictForAttr(filePath, attrIndx, isNumber):
    """
    This funciton returns a dictionary that store the row index set for all tuples
        that share the same value for attribute of index attrIndx
    Args:
        fileName
        attrIndx: the index of column that is considered as the key in file fileName
        isNumber: if the attribute is a number
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
            if row_ID == 0:#skip title
                row_ID += 1
                continue
            if isNumber:
                try:
                    key = float(rd[attrIndx])
                except:
                    try:#handle oscar.csv
                        key = float(rd[attrIndx].split('/')[0])
                    except:
                        key = 0.0
            else:
                key = rd[attrIndx]
#                 if key == '':
#                    key = 'NA'
            if key in dict_attr:
                #append row index w.r.t the tuple to the list
                dict_attr[key].append(row_ID)
            else:
                #create a list that store the row index w.r.t the tuple
                dict_attr[key] = [row_ID]
            row_ID += 1
        return dict_attr


def main():
    #a small unit test to check the functionality of index/btree creation
    fileName = 'oscars.csv'
    dataFilePath = './data/' + fileName
    filepathBtree = './btree/'
    attID = 3
    # build btrees for all attributes
    # buildTreeForAllAttr(fileName, dataFilePath, filepathBtree)
    btt = buildTreeForSingleAttr(fileName, dataFilePath, filepathBtree, AttrId = attID, return_tree = True, isNumber = True)
    # btt = buildTreeForMixedAttr(fileName, dataFilePath, filepathBtree, attrIndxSet = [0,5], Operator = "+", return_tree = True)


    # print(list(btt.keys()))
    #recover btree from btreeFile
    btreeFile = 'oscars_Attr_3_.tree'
    btree = recoverFromPickle(btreeFile, filepathBtree)
    print(list(btree.keys()))
    # print(list(btree.keys()))
    # print(list(btree.values('2')));
    # for k, it in btree.iteritems():
    #     print(k, it)
    # btree.items();

    # print()


start = time.time()
# main()


fileName1 = 'movies.csv'
dataFilePath1 = './data/' + fileName1
filepathBtree = './btree/'

# build btrees for all attributes
# buildTreeForAllAttr(fileName1, dataFilePath, filepathBtree)
# Testcase 1
#ID = getAttrID(dataFilePath1, 'director_name')
#btree1 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID, return_tree = True, isNumber = False)
#list1 = single_join_filter_one(btree1,'=','Ang Lee')
#
#ID = getAttrID(dataFilePath1, 'imdb_score')
#btree2 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID, return_tree = True, isNumber = True)
#list2 = single_join_filter_one(btree2,'>',7)
#
#list_1 = list1 + list2
#rows_1 = and_condition_single(list_1)

# Testcase 2
fileName2 = 'oscars.csv'
dataFilePath2 = './data/' + fileName2
#ID = getAttrID(dataFilePath2, 'Winner')
#btree3 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID, return_tree = True, isNumber = True)
#list3 = single_join_filter_one(btree3,'=',1)
#
#ID = getAttrID(dataFilePath2, 'Award')
#btree4 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID, return_tree = True, isNumber = False)
#list4 = single_join_filter_one(btree4,'=','Directing')
#
#list_2 = list3 + list4
#rows_2 = and_condition_single(list_2)
#
## Testcase 3
## SELECT title_year, movie_title, Award, imdb_score, movie_facebook_likes FROM movies M JOIN oscars A ON (M.movie_title = A.Film) 
## WHERE A.Winner = 1 AND (M.imdb_score < 6 OR M.movie_facebook_likes < 10000)
#ID1 = getAttrID(dataFilePath1, 'movie_title')
#btree5 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID1, return_tree = True, isNumber = False)
#ID2 = getAttrID(dataFilePath2, 'Film')
#btree6 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID2, return_tree = True, isNumber = False)
#list5 = double_join_filter(btree5,btree6,'=')
#
#list6 = list3
#
#ID1 = getAttrID(dataFilePath1, 'imdb_score')
#btree5 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID1, return_tree = True, isNumber = True)
#list7 = single_join_filter_one(btree5,'<',6)
#
#ID2 = getAttrID(dataFilePath1, 'movie_facebook_likes')
#btree6 = buildTreeForSingleAttr(fileName2, dataFilePath1, filepathBtree, AttrId = ID2, return_tree = True, isNumber = True)
#list8 = single_join_filter_one(btree6,'<',10000)
#
#list9 = or_condition_single(list7+list8)
#
#temp1 = single_to_double(list6)
#temp2 = single_to_double(list9)
#
#temp12 = list5
#out1 = and_condition_double(temp2,temp12,0,0)
#out2 = and_condition_double(temp1,out1,0,1)
#out3 = permute_list(out2)

# Testcase 6
# SELECT M.movie_title, M.title_year, M.imdb_score, A1.Name, A1.Award, A2.Name, A2.Award FROM movies M JOIN oscars A1 
# JOIN oscars A2 ON (M.movie_title = A1.Film AND M.movie_title = A2.Film) WHERE A1.Award = 'Actor' AND A2.Award = 'Actress';
ID1 = getAttrID(dataFilePath1, 'movie_title')
btree_mt = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID1, return_tree = True, isNumber = False)
#ID2 = getAttrID(dataFilePath1, 'title_year')
#btree_ty = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID2, return_tree = True, isNumber = True)
#ID3 = getAttrID(dataFilePath1, 'title_year')
#btree_is = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID3, return_tree = True, isNumber = True)

ID4 = getAttrID(dataFilePath2, 'Name')
btree_n1 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID4, return_tree = True, isNumber = False)
#ID5 = getAttrID(dataFilePath2, 'Award')
#btree_a1 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID5, return_tree = True, isNumber = False)
ID6 = getAttrID(dataFilePath2, 'Film')
btree_f1 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID6, return_tree = True, isNumber = False)

ID4 = getAttrID(dataFilePath2, 'Name')
btree_n2 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID4, return_tree = True, isNumber = False)
#ID5 = getAttrID(dataFilePath2, 'Award')
#btree_a2 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID5, return_tree = True, isNumber = False)
ID6 = getAttrID(dataFilePath2, 'Film')
btree_f2 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID6, return_tree = True, isNumber = False)

sout0 = single_join_filter_one(btree_a1,'=','Actor') # A1
sout1 = single_join_filter_one(btree_a2,'=','Actress') # A2
dout0 = double_join_filter(btree_mt,btree_f1,'=') # M_A1
dout1 = double_join_filter(btree_mt,btree_f2,'=') # M_A2

dout2 = single_to_double(sout0) # A1
dout3 = single_to_double(sout1) # A2

A1_M = and_condition_double(dout2,dout0,0,1)
A2_M = and_condition_double(dout3,dout1,0,1)
M_A1_A2 = and_condition_double(A1_M,A2_M,1,1)
out4 = permute_list(M_A1_A2)

'''
#recover btree from btreeFile
btreeFile1 = 'review-5k_Attr_1_.tree'
btree1 = recoverFromPickle(btreeFile1, filepathBtree)

fileName2 = 'review-20.csv'
dataFilePath = './data/' + fileName2
filepathBtree = './btree/'

# build btrees for all attributes
buildTreeForAllAttr(fileName2, dataFilePath, filepathBtree)
# btree1 = buildTreeForSingleAttr(fileName1, dataFilePath, filepathBtree, AttrId = 0, return_tree = True)

#recover btree from btreeFile
btreeFile2 = 'review-20_Attr_1_.tree'
btree2 = recoverFromPickle(btreeFile2, filepathBtree)

a1 = double_join_filter(btree1, btree2, '=')

btreeFile3 = 'review-20_Attr_5_.tree'
btree3 = recoverFromPickle(btreeFile3, filepathBtree)

btreeFile4 = 'review-5k_Attr_5_.tree'
btree4 = recoverFromPickle(btreeFile4, filepathBtree)
a2 = single_join_filter_one(btree3,'<',4)

a3 = list(btree3.values(min = btree3.minKey(), max = 4, excludemax=True))
print('time = ', time.time() - start)
'''
