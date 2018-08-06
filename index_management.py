import csv
from myCSV import *
from mybtree import *
# import gzip
import time
from select_and_print import *

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
#    with open(filePath, 'r', encoding="ISO-8859-1") as f:
#    a = time.time()
    with open(filePath, 'rb') as f:
        
        reader = csv.reader(f)
        dict_attr = {}
        f.seek(0)
        i = 0
        offset = 0
        offset_list = []
    #     dict_ = {}
        for line in f:
#             print(line, offset)
            offset += len(line)
            offset_list.append(offset)
#         print(offset_list)
        f.seek(0)
#    print(time.time() - a)
#    b = time.time()
#    print('len: ',len(offset_list))
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
#                 if key == '':
#                    key = 'NA'
            if key in dict_attr:
                #append row index w.r.t the tuple to the list
                dict_attr[key].append(offset_list[row_ID - 1])
            else:
                #create a list that store the row index w.r.t the tuple
                dict_attr[key] = [offset_list[row_ID - 1]]
            row_ID += 1
#         ct = 0
#         for k,v in dict_attr.items():
#             print(k,len(v))
#             ct += 1
#             if ct > 10:
#                 break
#         print(dict_attr[2006.0])
#        print(time.time() - b)
        return dict_attr
#
# def main():
#     #a small unit test to check the functionality of index/btree creation
#     fileName = 'oscars.csv'
#     dataFilePath = './data/' + fileName
#     filepathBtree = './btree/'
#     attID = 3
#     # build btrees for all attributes
#     # buildTreeForAllAttr(fileName, dataFilePath, filepathBtree)
#     btt = buildTreeForSingleAttr(fileName, dataFilePath, filepathBtree, AttrId = attID, return_tree = True, isNumber = True)
#     # btt = buildTreeForMixedAttr(fileName, dataFilePath, filepathBtree, attrIndxSet = [0,5], Operator = "+", return_tree = True)
#
#
#     # print(list(btt.keys()))
#     #recover btree from btreeFile
#     btreeFile = 'oscars_Attr_3_.tree'
#     btree = recoverFromPickle(btreeFile, filepathBtree)
#     print(list(btree.keys()))
    # print(list(btree.keys()))
    # print(list(btree.values('2')));
    # for k, it in btree.iteritems():
    #     print(k, it)
    # btree.items();

    # print()


# start = time.time()
# main()


#fileName1 = 'movies.csv'
#dataFilePath1 = './data/' + fileName1
#filepathBtree = './btree/'
#
#
# #Testcase 1
# ID = getAttrID(dataFilePath1, 'director_name')
# btree1 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID, return_tree = True, isNumber = False)
# list1 = single_join_filter_one(btree1,'=','ANG LEE')
#
# ID = getAttrID(dataFilePath1, 'imdb_score')
# btree2 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID, return_tree = True, isNumber = True)
# list2 = single_join_filter_one(btree2,'>',7)
#
# list_1 = list1 + list2
# out = and_condition_single(list_1)
#
# # Testcase 2
#fileName2 = 'oscars.csv'
#dataFilePath2 = './data/' + fileName2
#ID = getAttrID(dataFilePath2, 'Winner')
#btree3 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID, return_tree = True, isNumber = True)
#list3 = single_join_filter_one(btree3,'=',1)

#ID = getAttrID(dataFilePath2, 'Award')
#btree4 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID, return_tree = True, isNumber = False)
#start = time.time()
#list4 = single_join_filter_one(btree4,'=','DIRECTING')
#
#list_2 = list3 + list4
#out = and_condition_single(list_2)
#print(time.time() - start)
#
# Testcase 3
# SELECT title_year, movie_title, Award, imdb_score, movie_facebook_likes FROM movies M JOIN oscars A ON (M.movie_title = A.Film) 
# WHERE A.Winner = 1 AND (M.imdb_score < 6 OR M.movie_facebook_likes < 10000)
#start = time.time()
#ID1 = getAttrID(dataFilePath1, 'movie_title')
#btree5 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID1, return_tree = True, isNumber = False)
#ID2 = getAttrID(dataFilePath2, 'Film')
#btree6 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID2, return_tree = True, isNumber = False)
#list5 = double_join_filter(btree5,btree6,'=')
#
#ID1 = getAttrID(dataFilePath1, 'imdb_score')
#btree5 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID1, return_tree = True, isNumber = True)
#list7 = single_join_filter_one(btree5,'<',6)
#
#ID2 = getAttrID(dataFilePath1, 'movie_facebook_likes')
#btree6 = buildTreeForSingleAttr(fileName2, dataFilePath1, filepathBtree, AttrId = ID2, return_tree = True, isNumber = True)
#list8 = single_join_filter_one(btree6,'<',10000)
#
#temp1 = list3
#temp2 = or_condition_single(list7+list8)
#temp12 = list5
#out1 = A_AB_B_and(temp2,temp12,temp1)
#out2 = cross_prod(out1)
#out = permute_list(out2)
#print(time.time() - start)

# Testcase 4
# SELECT A1.Year, A1.Film, A1.Award, A1.Name, A2.Award, A2.Name FROM oscars A1 JOIN oscars A2 ON (A1.Film = A2.Film) 
# WHERE A1.Film <> '' AND A1.Winner = 1 AND A2.Winner=1 AND A1.Award > A2.Award AND A1.Year > 2010;
#ID1 = getAttrID(dataFilePath2, 'Film')
#btree_f1 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID1, return_tree = True, isNumber = False)
#ID2 = getAttrID(dataFilePath2, 'Film')
#btree_f2 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID2, return_tree = True, isNumber = False)
#ID3 = getAttrID(dataFilePath2, 'Winner')
#btree_w1 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID3, return_tree = True, isNumber = True)
#ID4 = getAttrID(dataFilePath2, 'Winner')
#btree_w2 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID4, return_tree = True, isNumber = True)
#ID5 = getAttrID(dataFilePath2, 'Award')
#btree_a1 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID5, return_tree = True, isNumber = False)
#ID6 = getAttrID(dataFilePath2, 'Award')
#btree_a2 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID6, return_tree = True, isNumber = False)
#ID7 = getAttrID(dataFilePath2, 'Year')
#btree_y1 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID7, return_tree = True, isNumber = True)
#
#start1 = time.time()
#
#list_f1 = single_join_filter_one(btree_f1,'<>','')
#list_w1 = single_join_filter_one(btree_w1,'=',1)
#list_w2 = single_join_filter_one(btree_w2,'=',1)
#list_y1 = single_join_filter_one(btree_y1,'>',2010)
#A1 = and_condition_single(list_f1 + list_w1 + list_y1)
#B1 = list_w2
#path = 'oscars.csv'
#btree_temp_a1 = get_small_btree(path, A1, ID5, 0)
#btree_temp_f1 = get_small_btree(path, A1, ID1, 0)
#btree_temp_a2 = get_small_btree(path, B1, ID5, 0)
#btree_temp_f2 = get_small_btree(path, B1, ID1, 0)
#start2 = time.time()
#list1 = double_join_filter(btree_temp_a2,btree_temp_a1,'<')
#list2 = double_join_filter(btree_temp_f1,btree_temp_f2,'=')
## print(len(list1[0]))
## print(len(list2[0]))
##start3 = time.time()
##list_BA = double_join_filter(btree_a2,btree_a1,'<') # BA
##list_AB = double_join_filter(btree_f1,btree_f2,'=') # AB
##print(time.time() - start3)
##print(len(list1))
#A1, B1 = get_A_B_AB_or(list1)
#A2, B2 = get_A_B_AB_or(list2)
#A3 = and_condition_single(A1 + A2)
#B3 = and_condition_single(B1 + B2)
#
#BA = A_AB_B_and(A3, list1, B3)
#AB = A_AB_B_and(A3, list2, B3)
#
#[temp12,temp11] = AB_AC(AB,BA,0,1)
#[temp12,temp11] = AB_AC(AB,BA,1,0)
#temp21 = cross_prod(temp11) # BA
#temp22 = cross_prod(temp12) # AB
#out1 = AB_AB(temp22, temp21, 0)
#out = permute_list(out1)
#
#print(time.time() - start1)







# start = time.time()
# list_5_1 = double_join_filter(btree_f1,btree_f2,'=') # AB
# list_5_2 = single_join_filter_one(btree_f1,'<>','')
# list_5_3 = single_join_filter_one(btree_w1,'=',1)
# list_5_4 = single_join_filter_one(btree_w2,'=',1)
# list_5_5 = double_join_filter(btree_a2,btree_a1,'<') # BA
# list_5_6 = single_join_filter_one(btree_y1,'>',2010)
#
# temp1 = and_condition_single(list_5_2+list_5_3+list_5_6)
# temp2 = list_5_4
# temp11 = A_AB_B_and(temp1,list_5_5,temp2) # BA
# temp12 = A_AB_B_and(temp1,list_5_1,temp2) # AB
# [temp12,temp11] = AB_AC(temp12,temp11,0,1)
# [temp12,temp11] = AB_AC(temp12,temp11,1,0)
# temp21 = cross_prod(temp11) # BA
# temp22 = cross_prod(temp12) # AB
#
# out1 = AB_AB(temp22, temp21, 0)
# out = permute_list(out1)
#
# print(time.time() - start)




# Testcase 5
# SELECT M1.director_name, M1.title_year, M1.movie_title, M2.title_year, M2.movie_title, M3.title_year, 
# M3.movie_title FROM movies M1 JOIN movies M2 JOIN movies M3 ON 
# (M1.director_name = M2.director_name AND M1.director_name = M3.director_name) 
# WHERE M1.movie_title <> M2.movie_title AND M2.movie_title <> M3.movie_title AND 
# M1.movie_title <> M3.movie_title AND M1.title_year < M2.title_year-15 AND M2.title_year < M3.title_year-15
#ID1 = getAttrID(dataFilePath1, 'movie_title')
#btree_mt1 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID1, return_tree = True, isNumber = False)
#ID2 = getAttrID(dataFilePath1, 'movie_title')
#btree_mt2 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID2, return_tree = True, isNumber = False)
#ID3 = getAttrID(dataFilePath1, 'movie_title')
#btree_mt3 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID3, return_tree = True, isNumber = False)
#ID4 = getAttrID(dataFilePath1, 'director_name')
#btree_dn1 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID4, return_tree = True, isNumber = False)
#ID5 = getAttrID(dataFilePath1, 'director_name')
#btree_dn2 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID5, return_tree = True, isNumber = False)
#ID6 = getAttrID(dataFilePath1, 'director_name')
#btree_dn3 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID6, return_tree = True, isNumber = False)
#ID7 = getAttrID(dataFilePath1, 'title_year')
#btree_ty1 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID7, return_tree = True, isNumber = True)
#ID8 = getAttrID(dataFilePath1, 'title_year')
#btree_ty2 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID8, return_tree = True, isNumber = True)
#ID9 = getAttrID(dataFilePath1, 'title_year')
#btree_ty3 = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID9, return_tree = True, isNumber = True)
#
#t1 = time.time()
#listab1 = double_join_filter(btree_dn1, btree_dn2, '=')
#listac1 = double_join_filter(btree_dn1, btree_dn3, '=')
#listab2 = double_join_filter_plus(btree_ty1,btree_ty2,'<',15)
#listbc1 = double_join_filter_plus(btree_ty2,btree_ty3,'<',15)
#
#a1, b1 = get_A_B_AB_or(listab1)
#a2, b2 = get_A_B_AB_or(listab2)
#b3, c1 = get_A_B_AB_or(listbc1)
#a3, c2 = get_A_B_AB_or(listac1)
#a = and_condition_single(a1+a2+a3)
#b = and_condition_single(b1+b2+b3) 
#c = and_condition_single(c1+c2) 
#
#AB1 = A_AB_B_and(a, listab1, b)
#AC = A_AB_B_and(a, listac1, c)
#AB2 = A_AB_B_and(a, listab2, b)
#BC = A_AB_B_and(b, listbc1, c)
#
#ab1 = cross_prod(AB1)
#ab2 = cross_prod(AB2)
#ac = cross_prod(AC)
#bc = cross_prod(BC)
#ab_list = AB_AC(ab1, ab2, 0, 0)
#abac = AB_AC(ab_list[0], bc, 1, 0)
#out = and_condition_double(abac[0], ac, 0, 0)
#
#print(time.time() - t1)



#btree_a_mt = get_small_btree(dataFilePath1, a, ID1, 0)
#btree_b_mt = get_small_btree(dataFilePath1, b, ID1, 0)
#btree_c_mt = get_small_btree(dataFilePath1, c, ID1, 0)

#ac = double_join_filter(btree_a_mt, btree_c_mt, '<>')
'''
bc = double_join_filter(btree_b_mt, btree_c_mt, '<>')
#ab = double_join_filter(btree_a_mt, btree_b_mt, '<>')

a1, b1 = get_A_B_AB_or(ab)
a2, c1 = get_A_B_AB_or(ac)
b2, c2 = get_A_B_AB_or(bc)
a = and_condition_single(a1 + a2 + a3)
b = and_condition_single(b1 + b2 + b3)

A_AB_B_and(a, list1, b)

print(time.time() - t1)
'''
#start = time.time()
#listab1 = double_join_filter(btree_dn1, btree_dn2, '=')
##listac1 = double_join_filter(btree_mt1, btree_mt3, '<>')
##listbc1 = double_join_filter(btree_mt2, btree_mt3, '<>')
#listac2 = double_join_filter(btree_mt1, btree_mt3, '<>')
#listab2 = double_join_filter_plus(btree_ty1,btree_ty2,'<',15)
#listbc2 = double_join_filter_plus(btree_ty2,btree_ty3,'<',15)
#print(time.time() - start)





# # Testcase 6
# # SELECT M.movie_title, M.title_year, M.imdb_score, A1.Name, A1.Award, A2.Name, A2.Award FROM movies M JOIN oscars A1
# # JOIN oscars A2 ON (M.movie_title = A1.Film AND M.movie_title = A2.Film) WHERE A1.Award = 'Actor' AND A2.Award = 'Actress';
# ID1 = getAttrID(dataFilePath1, 'movie_title')
# btree_mt = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID1, return_tree = True, isNumber = False)
# ID2 = getAttrID(dataFilePath1, 'title_year')
# btree_ty = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID2, return_tree = True, isNumber = True)
# ID3 = getAttrID(dataFilePath1, 'title_year')
# btree_is = buildTreeForSingleAttr(fileName1, dataFilePath1, filepathBtree, AttrId = ID3, return_tree = True, isNumber = True)
#
# ID4 = getAttrID(dataFilePath2, 'Name')
# btree_n1 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID4, return_tree = True, isNumber = False)
# ID5 = getAttrID(dataFilePath2, 'Award')
# btree_a1 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID5, return_tree = True, isNumber = False)
# ID6 = getAttrID(dataFilePath2, 'Film')
# btree_f1 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID6, return_tree = True, isNumber = False)
#
# ID4 = getAttrID(dataFilePath2, 'Name')
# btree_n2 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID4, return_tree = True, isNumber = False)
# ID5 = getAttrID(dataFilePath2, 'Award')
# btree_a2 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID5, return_tree = True, isNumber = False)
# ID6 = getAttrID(dataFilePath2, 'Film')
# btree_f2 = buildTreeForSingleAttr(fileName2, dataFilePath2, filepathBtree, AttrId = ID6, return_tree = True, isNumber = False)
#
# A1 = single_join_filter_one(btree_a1,'=','ACTOR') # A1
# A2 = single_join_filter_one(btree_a2,'=','ACTRESS') # A2
# M_A1 = double_join_filter(btree_mt,btree_f1,'=') # M_A1
# M_A2 = double_join_filter(btree_mt,btree_f2,'=') # M_A2
#
# start = time.time()
# out1 = A_AB_and(A1, M_A1, 1) # M_A1
# out2 = A_AB_and(A2, M_A2, 1) # M_A2
# [out1,out2] = AB_AC(out1,out2,0,1)
# out3 = cross_prod(out1)
# out4 = cross_prod(out2)
#
# out5 = and_condition_double(out3,out4,0,0) # M_A1_A2
# out = permute_list(out5)
# print(time.time() - start)










#==================================================================================================================================#
#1
#alias_index_result = ['M']
#rowindice_result_from_selection = out
#sql_statement = "SELECT M.movie_title, M.title_year, M.imdb_score FROM movies.csv M WHERE M.director_name = 'Ang Lee' AND imdb_score > 7"
#ProjectAndPrint(sql_statement, rowindice_result_from_selection, alias_index_result)

#2
#alias_index_result = ['A']
#rowindice_result_from_selection = out
#sql_statement = "SELECT A.Year, A.Film, A.Name FROM oscars.csv A WHERE A.Winner= 1 and A.Award = 'Directing'"
#ProjectAndPrint(sql_statement, rowindice_result_from_selection, alias_index_result)


#3
#alias_index_result = ['M','A']
#rowindice_result_from_selection = out
#sql_statement = "SELECT M.title_year, M.movie_title, A.Award, M.imdb_score, M.movie_facebook_likes FROM movies.csv M JOIN oscars.csv A ON (M.movie_title = A.Film) WHERE A.Winner = 1 AND (M.imdb_score < 6 OR M.movie_facebook_likes < 10000)"
#ProjectAndPrint(sql_statement, rowindice_result_from_selection, alias_index_result)


#4
# alias_index_result = ['A1','A2']
# rowindice_result_from_selection = out
# sql_statement = "SELECT A1.Year, A1.Film, A1.Award, A1.Name, A2.Award, A2.Name FROM oscars.csv A1 JOIN oscars.csv A2 ON (A1.Film = A2.Film) WHERE A1.Film <> '' AND A1.Winner = 1 AND A2.Winner=1 AND A1.Award > A2.Award AND A1.Year > 2010"
# ProjectAndPrint(sql_statement, rowindice_result_from_selection, alias_index_result)


#6
#alias_index_result = ['M','A1','A2']
#rowindice_result_from_selection = out
#sql_statement = "SELECT M.movie_title, M.title_year, M.imdb_score, A1.Name, A1.Award, A2.Name, A2.Award FROM movies.csv M JOIN oscars.csv A1 JOIN oscars.csv A2 ON (M.movie_title = A1.Film AND M.movie_title = A2.Film) WHERE A1.Award = 'Actor' AND A2.Award = 'Actress'"
#ProjectAndPrint(sql_statement, rowindice_result_from_selection, alias_index_result)


#
# fileName_1 = 'review-1m.csv'
# dataFilePath_1 = './data/' + fileName_1
# filepathBtree_1 = './btree/'
# fileName_2 = 'business.csv'
# dataFilePath_2 = './data/' + fileName_2
# filepathBtree_2 = './btree/'
# fileName_3 = 'photos.csv'
# dataFilePath_3 = './data/' + fileName_3
# filepathBtree_3 = './btree/'


# ==================================================================================================================================#
#TestCase 1
#SELECT R.review_id, R.funny, R.useful FROM review-1m.csv R WHERE R.funny >= 20 AND R.useful > 30
#ID1 = getAttrID(dataFilePath_1, 'funny')
#btree1 = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID1, return_tree = True, isNumber = True)
#ID2 = getAttrID(dataFilePath_1, 'useful')
#btree2 = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID2, return_tree = True, isNumber = True)
#
#start = time.time()
#list1 = single_join_filter_one(btree1,'>=',20)
#list2 = single_join_filter_one(btree2,'>',30)
#
#list_1 = list1 + list2
#out = and_condition_single(list_1)
#print(time.time() - start)
# ==================================================================================================================================#



# ==================================================================================================================================#
#TestCase 2
#SELECT B.name, B.city, B.state FROM business.csv B WHERE B.city = 'Champaign' AND B.state = 'IL'
#ID1 = getAttrID(dataFilePath_2, 'city')
#btree1 = buildTreeForSingleAttr(fileName_2, dataFilePath_2, filepathBtree_2, AttrId = ID1, return_tree = True, isNumber = False)
#ID2 = getAttrID(dataFilePath_2, 'state')
#btree2 = buildTreeForSingleAttr(fileName_2, dataFilePath_2, filepathBtree_2, AttrId = ID2, return_tree = True, isNumber = False)
#
#start = time.time()
#list1 = single_join_filter_one(btree1,'=','CHAMPAIGN')
#list2 = single_join_filter_one(btree2,'=','IL')
#
#list_1 = list1 + list2
#out = and_condition_single(list_1)
#print(time.time() - start)
# ==================================================================================================================================#



# ==================================================================================================================================#
#TestCase 3
#SELECT B.name, B.postal_code, R.stars, R.useful FROM business.csv B JOIN review-1m.csv R ON (B.business_id = R.business_id) 
#WHERE B.name = 'Sushi Ichiban' AND B.postal_code = '61820'
#ID1 = getAttrID(dataFilePath_1, 'business_id')
#btree1 = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID1, return_tree = True, isNumber = False)
#ID2 = getAttrID(dataFilePath_2, 'business_id')
#btree2 = buildTreeForSingleAttr(fileName_2, dataFilePath_2, filepathBtree_2, AttrId = ID2, return_tree = True, isNumber = False)
#ID3 = getAttrID(dataFilePath_2, 'name')
#btree3 = buildTreeForSingleAttr(fileName_1, dataFilePath_2, filepathBtree_2, AttrId = ID3, return_tree = True, isNumber = False)
#ID4 = getAttrID(dataFilePath_2, 'postal_code')
#btree4 = buildTreeForSingleAttr(fileName_2, dataFilePath_2, filepathBtree_2, AttrId = ID4, return_tree = True, isNumber = False)
#
#start = time.time()
#B1 = single_join_filter_one(btree3,'=','SUSHI ICHIBAN')
#B2 = single_join_filter_one(btree4,'=','61820')
#B = and_condition_single(B1 + B2)
#
## file and btree
#BR = btree_A_a_file(btree1, dataFilePath_2, B, ID2, '=', 0)
#
## reconstructed btree and file
#btree_small = get_small_btree(dataFilePath_2, B, ID2, 0)
#BR = double_join_filter(btree_small, btree1, '=')
#
#temp = A_AB_and(B, BR, 0)
#out1 = cross_prod(temp)
#out = permute_list(out1) 
#print(time.time() - start)
# ==================================================================================================================================#




# ==================================================================================================================================#
#TestCase 4
#SELECT R1.user_id, R2.user_id, R1.stars, R2.stars FROM review-1m.csv R1 JOIN review-1m.csv R2 ON (R1.business_id = R2.business_id) 
#WHERE R1.stars = 5 AND R2.stars = 1 AND R1.useful > 50 AND R2.useful > 50
#ID1 = getAttrID(dataFilePath_1, 'business_id')
#btree1 = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID1, return_tree = True, isNumber = False)
#ID2 = getAttrID(dataFilePath_1, 'business_id')
#btree2 = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID2, return_tree = True, isNumber = False)
#ID3 = getAttrID(dataFilePath_1, 'stars')
#btree3 = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID3, return_tree = True, isNumber = True)
#ID4 = getAttrID(dataFilePath_1, 'stars')
#btree4 = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID4, return_tree = True, isNumber = True)
#ID5 = getAttrID(dataFilePath_1, 'useful')
#btree5 = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID5, return_tree = True, isNumber = True)
#ID6 = getAttrID(dataFilePath_1, 'useful')
#btree6 = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID6, return_tree = True, isNumber = True)
#
#start = time.time()
#R1_1 = single_join_filter_one(btree3,'=',5)
#R2_1 = single_join_filter_one(btree4,'=',1)
#R1_2 = single_join_filter_one(btree5,'>',50)
#R2_2 = single_join_filter_one(btree6,'>',50)
#
#R1 = and_condition_single(R1_1 + R1_2)
#R2 = and_condition_single(R2_1 + R2_2)
#R1R2 = A_a_B_b_file(dataFilePath_1, R1, ID1, dataFilePath_1, R2, ID2, '=', False)
#out1 = cross_prod(R1R2)
#out = permute_list(out1)
#print(time.time()-start)
# ==================================================================================================================================#






# ==================================================================================================================================#
#TestCase 5
#SELECT B.name, B.city, B.state, R.stars, P.label FROM business.csv B JOIN review-1m.csv R JOIN photos.csv P 
#ON (B.business_id = R.business_id AND B.business_id = P.business_id) 
#WHERE B.city = 'Champaign' AND B.state = 'IL' AND R.stars = 5 AND P.label = 'inside'
#ID1 = getAttrID(dataFilePath_1, 'business_id')
#btree_rid = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID1, return_tree = True, isNumber = False)
#
#ID2 = getAttrID(dataFilePath_1, 'stars')
#btree_rstar = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID2, return_tree = True, isNumber = True)
#
#ID3 = getAttrID(dataFilePath_2, 'business_id')
#btree_bid = buildTreeForSingleAttr(fileName_2, dataFilePath_2, filepathBtree_2, AttrId = ID3, return_tree = True, isNumber = False)
#
#ID4 = getAttrID(dataFilePath_2, 'city')
#btree_bcity = buildTreeForSingleAttr(fileName_2, dataFilePath_2, filepathBtree_2, AttrId = ID4, return_tree = True, isNumber = False)
#
#ID5 = getAttrID(dataFilePath_2, 'state')
#btree_bstate = buildTreeForSingleAttr(fileName_2, dataFilePath_2, filepathBtree_2, AttrId = ID5, return_tree = True, isNumber = False)
#
#ID6 = getAttrID(dataFilePath_3, 'business_id')
#btree_pid = buildTreeForSingleAttr(fileName_3, dataFilePath_3, filepathBtree_3, AttrId = ID6, return_tree = True, isNumber = False)
#
#ID7 = getAttrID(dataFilePath_3, 'label')
#btree_plabel = buildTreeForSingleAttr(fileName_3, dataFilePath_3, filepathBtree_3, AttrId = ID7, return_tree = True, isNumber = False)
#
#start = time.time()
#B1 = single_join_filter_one(btree_bcity,'=','CHAMPAIGN')
#B2 = single_join_filter_one(btree_bstate,'=','IL')
#R = single_join_filter_one(btree_rstar,'=',5)
#P = single_join_filter_one(btree_plabel,'=','INSIDE')
#B = and_condition_single(B1 + B2)
#
#btree_small_r = get_small_btree(dataFilePath_1, R, ID1, 0)
#btree_small_b = get_small_btree(dataFilePath_2, B, ID3, 0)
#btree_small_p = get_small_btree(dataFilePath_3, P, ID6, 0)
#BR = double_join_filter(btree_small_b, btree_small_r, '=')
#BP = double_join_filter(btree_small_b, btree_small_p, '=')
#br = cross_prod(BR)
#bp = cross_prod(BP)
#out1 = and_condition_double(br, bp, 0, 0)
#out = permute_list(out1)
##BR = A_a_B_b_file(dataFilePath_2, B, ID2, dataFilePath_1, R, ID1, '=', 0)
##BP = A_a_B_b_file(dataFilePath_2, B, ID2, dataFilePath_3, P, ID6, '=', 0)
#
#print(time.time() - start)
# ==================================================================================================================================#






# ==================================================================================================================================#
#TestCase 6
#SELECT B.name, R1.user_id, R2.user_id FROM business.csv B JOIN review-1m.csv R1 JOIN review-1m.csv R2 ON (B.business_id = R1.business_id 
#AND R1.business_id = R2.business_id) WHERE R1.stars = 5 AND R2.stars = 1 AND R1.useful > 50 AND R2.useful > 50
# ID1 = getAttrID(dataFilePath_1, 'business_id')
# btree_r1id = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID1, return_tree = True, isNumber = False)
# ID2 = getAttrID(dataFilePath_1, 'business_id')
# btree_r2id = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID2, return_tree = True, isNumber = False)
# ID3 = getAttrID(dataFilePath_2, 'business_id')
# btree_bid = buildTreeForSingleAttr(fileName_2, dataFilePath_2, filepathBtree_2, AttrId = ID3, return_tree = True, isNumber = False)
# ID4 = getAttrID(dataFilePath_1, 'stars')
# btree_r1star = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID4, return_tree = True, isNumber = True)
# ID5 = getAttrID(dataFilePath_1, 'stars')
# btree_r2star = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID5, return_tree = True, isNumber = True)
# ID6 = getAttrID(dataFilePath_1, 'useful')
# btree_r1useful = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID6, return_tree = True, isNumber = True)
# ID7 = getAttrID(dataFilePath_1, 'useful')
# btree_r2useful = buildTreeForSingleAttr(fileName_1, dataFilePath_1, filepathBtree_1, AttrId = ID7, return_tree = True, isNumber = True)
#
# start = time.time()
# R1_1 = single_join_filter_one(btree_r1star,'=',5)
# R2_1 = single_join_filter_one(btree_r2star,'=',1)
# R1_2 = single_join_filter_one(btree_r1useful,'>',50)
# R2_2 = single_join_filter_one(btree_r2useful,'>',50)
# R1 = and_condition_single(R1_1 + R1_2)
# R2 = and_condition_single(R2_1 + R2_2)
# R1R2 = A_a_B_b_file(dataFilePath_1, R1, ID1, dataFilePath_1, R2, ID2, '=', 0)
# R2B = A_a_btree_file(dataFilePath_1, R2, ID2, btree_bid, '=', 0)
# r1r2 = cross_prod(R1R2)
# r2b = cross_prod(R2B)
# out1 = and_condition_double(r1r2, r2b, 1, 0)
# out = permute_list(out1)
#
# print(time.time() - start)
# ==================================================================================================================================#
















