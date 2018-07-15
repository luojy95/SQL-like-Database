import time
import itertools
from itertools import product
from myCSV import *
from mybtree import *
    
def single_join_filter_one(btree, operator, value):
    '''

    '''
    if operator == '<':
        value_list = list(btree.values(min = btree.minKey(), max = value, excludemax=True))
    if operator == '<=':
        value_list = list(btree.values(min = btree.minKey(), max = value))
    if operator == '>':
        value_list = list(btree.values(min = value, max = btree.maxKey(), excludemin=True))
    if operator == '>=':
        value_list = list(btree.values(min = value, max = btree.maxKey()))
    if operator == '=':
        value_list = btree.get(value)
    # key_list = list(btree.keys())
    return value_list

# def single_join_filter_more(btree_list, operator_list, value_list):
    '''
  
    '''
    # attr_list = getAttrList(filepathBtree + btreeFile_list[0])
    # btree = recoverFromPickle(btreeFile_list[0], filepathBtree)
    # key_list = list(btree.keys())
    # index = 0
    # join_attr_list_ = []
    # for i in len(btree_list):
    #    if attr_list[i] == join_attr_list[index]:
    #        join_attr_list_.append(i)
    #        index += 1
    # pri_result = []
    # for i in len(btree_list):
    #     temp = single_join_filter_one(btree_list[i], operator_list[i], value_list[i])
    #     pri_result.append(temp)
    # output = pri_result[0]
    # for m in len(pri_result):
    #     output = set(pri_result[i]) & output
    # return output

def double_join_filter(btree1, btree2, operator):
    '''
 
    '''
    list1 = list(btree1.keys())
    list2 = list(btree2.keys())
    i = 0
    j = 0
    output = []
    if operator == '<':
        while (i <= len(list1) - 1 and j <= len(list2)):
            if list1[i] < list2[j]:
                print(list(list(itertools.product([list1[i]], list2[j:len(list2)]))))
                output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                if j < len(list2) - 1:
                    j += 1
            i += 1

    if operator == '<=':
        while (i <= len(list1) - 1 and j <= len(list2)):
            if list1[i] <= list2[j]:
                output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                if j < len(list2) - 1:
                    j += 1
            i += 1
    
    if operator == '=':
        while (i <= len(list1) - 1 and j <= len(list2)):
            if list1[i] == list2[j]:
                output = output + list(list(itertools.product([list1[i]], [list2[j]])))
                if j < len(list2) - 1:
                    j += 1
            i += 1
    
    out = []
    for i in len(output):
        out = out + list(itertools.product(output[i][0], output[i][1]))
    
    row_list = [[item[0], item[1]] for item in output]
    return row_list

def and_condition(list_row_list):
    '''
    
    '''
    output = list_row_list[0]
    for i in len(list_row_list):
        output = set(list_row_list[i]).intersection(output)
    return list(output)

def or_condition(list_row_list):
    '''
    
    '''
    output = list_row_list[0]
    for i in len(list_row_list):
        output = set(list_row_list[i]).union(output)
    return list(output)  

def except_condition(list_row_list):
    '''
    
    '''
    output = list_row_list[0]
    for i in len(list_row_list):
        output = set(list_row_list[i]).difference(output)
    return list(output)  
         
                
                
                
    
    
    
    
