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
    elif operator == '<=':
        value_list = list(btree.values(min = btree.minKey(), max = value))
    elif operator == '>':
        value_list = list(btree.values(min = value, max = btree.maxKey(), excludemin=True))
    elif operator == '>=':
        value_list = list(btree.values(min = value, max = btree.maxKey()))
    elif operator == '=':
        value_list = btree.get(value)
    else:
        print('invalid operator')
        value_list = []
    output = []
    for i in range(len(value_list)):
        output = output + value_list[i]
    # key_list = list(btree.keys())
    return [output]

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

def double_join_filter_plus(btree1, btree2, operator, value):
    '''
 
    '''
    list1 = list(btree1.keys())
    list2 = list(btree2.keys())
    i = 0
    j = 0
    output = []
    if operator == '<':
        while (i < len(list1) - 1 or j < len(list2) - 1):
            if i == len(list1) - 1:
                if list1[i] < list2[j] + value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                j += 1
            elif j == len(list2) - 1:
                if list1[i] < list2[j] + value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                i += 1
            else:
                if list1[i] < list2[j] + value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                    i += 1
                else: 
                    j += 1

    if operator == '<=':
        while (i < len(list1) - 1 or j < len(list2) - 1):
            if i == len(list1) - 1:
                if list1[i] <= list2[j] + value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                j += 1
            elif j == len(list2) - 1:
                if list1[i] <= list2[j] + value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                i += 1
            else:
                if list1[i] <= list2[j] + value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                    i += 1
                else: 
                    j += 1
    
    if operator == '=':
        while (i <= len(list1) - 1 and j <= len(list2) - 1):
            if i == len(list1) - 1:
                if list1[i] == list2[j] + value:
                    output = output + [[list1[i], list2[j]]]
                j += 1
            elif j == len(list2) - 1:
                if list1[i] == list2[j] + value:
                    output = output + [[list1[i], list2[j]]]
                i += 1
            else:
                if list1[i] == list2[j] + value:
                    output = output + [[list1[i], list2[j]]]
                if list1[i] < list2[j]:
                    i += 1
                else: 
                    j += 1
    
    row_list = [[btree1[item[0]], btree2[item[1]]] for item in output]
    
    return row_list

def double_join_filter(btree1, btree2, operator):
    '''
 
    '''
    list1 = list(btree1.keys())
    list2 = list(btree2.keys())
    i = 0
    j = 0
    output = []
    if operator == '<':
        while (i < len(list1) - 1 or j < len(list2) - 1):
            if i == len(list1) - 1:
                if list1[i] < list2[j]:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                j += 1
            elif j == len(list2) - 1:
                if list1[i] < list2[j]:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                i += 1
            else:
                if list1[i] < list2[j]:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                    i += 1
                else: 
                    j += 1

    if operator == '<=':
        while (i < len(list1) - 1 or j < len(list2) - 1):
            if i == len(list1) - 1:
                if list1[i] <= list2[j]:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                j += 1
            elif j == len(list2) - 1:
                if list1[i] <= list2[j]:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                i += 1
            else:
                if list1[i] <= list2[j]:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                    i += 1
                else: 
                    j += 1
    
    if operator == '=':
        while (i <= len(list1) - 1 and j <= len(list2) - 1):
            if i == len(list1) - 1:
                if list1[i] == list2[j]:
                    output = output + [[list1[i], list2[j]]]
                j += 1
            elif j == len(list2) - 1:
                if list1[i] == list2[j]:
                    output = output + [[list1[i], list2[j]]]
                i += 1
            else:
                if list1[i] == list2[j]:
                    output = output + [[list1[i], list2[j]]]
                if list1[i] < list2[j]:
                    i += 1
                else: 
                    j += 1
    
    
    row_list = [[btree1[item[0]], btree2[item[1]]] for item in output]
    
    return row_list

def double_join_filter_multi(btree1, btree2, operator, value):
    '''
 
    '''
    list1 = list(btree1.keys())
    list2 = list(btree2.keys())
    i = 0
    j = 0
    output = []
    if operator == '<':
        while (i < len(list1) - 1 or j < len(list2) - 1):
            if i == len(list1) - 1:
                if list1[i] < list2[j] * value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                j += 1
            elif j == len(list2) - 1:
                if list1[i] < list2[j] * value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                i += 1
            else:
                if list1[i] < list2[j] * value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                    i += 1
                else: 
                    j += 1

    if operator == '<=':
        while (i < len(list1) - 1 or j < len(list2) - 1):
            if i == len(list1) - 1:
                if list1[i] <= list2[j] * value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                j += 1
            elif j == len(list2) - 1:
                if list1[i] <= list2[j] * value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                i += 1
            else:
                if list1[i] <= list2[j] * value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                    i += 1
                else: 
                    j += 1
    
    if operator == '=':
        while (i <= len(list1) - 1 and j <= len(list2) - 1):
            if i == len(list1) - 1:
                if list1[i] == list2[j] * value:
                    output = output + [[list1[i], list2[j]]]
                j += 1
            elif j == len(list2) - 1:
                if list1[i] == list2[j] * value:
                    output = output + [[list1[i], list2[j]]]
                i += 1
            else:
                if list1[i] == list2[j] * value:
                    output = output + [[list1[i], list2[j]]]
                if list1[i] < list2[j]:
                    i += 1
                else: 
                    j += 1
    
    row_list = [[btree1[item[0]], btree2[item[1]]] for item in output]
    return row_list

def and_condition_single(list_row_list):
    '''
    
    '''
    output = list_row_list[0]
    for i in range(len(list_row_list)):
        output = set(list_row_list[i]).intersection(output)
    return list(output)

def or_condition_single(list_row_list):
    '''
    
    '''
    output = list_row_list[0]
    for i in range(len(list_row_list)):
        output = set(list_row_list[i]).union(output)
    return list(output)  

def except_condition_single(list_row_list):
    '''
    list_ror_list is a two_value tuple.
    '''
    output = list_row_list[0]
    for i in range(len(list_row_list)):
        output = set(list_row_list[i]).difference(output)
    return list(output)  

def and_condition_double(list_row_list1, list_row_list2):
    '''
    The first value of each list is the same.
    list_ror_list2 is a two_value tuple.
    '''
    output = []
    for i in range(len(list_row_list1)):
        for j in range(len(list_row_list2)):
            if list_row_list1[i][0] == list_row_list2[j][0]:
                temp = list_row_list1[i] + [list_row_list2[j][1]]
                output.append(temp)
    return output



list1 = [1,5,6,7]
list2 = [4,6]
output = []
i = 0
j = 0
operator = '='
if operator == '=':
    while (i <= len(list1) - 1 and j <= len(list2) - 1):
        if i == len(list1) - 1:
            if list1[i] == list2[j]:
                output = output + [[list1[i], list2[j]]]
            j += 1
        elif j == len(list2) - 1:
            if list1[i] == list2[j]:
                output = output + [[list1[i], list2[j]]]
            i += 1
        else:
            if list1[i] == list2[j]:
                output = output + [[list1[i], list2[j]]]
            if list1[i] < list2[j]:
                i += 1
            else: 
                j += 1