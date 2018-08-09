import itertools
import os
import sys
from myCSV import *
from mybtree import *
    
def single_join_filter_one(btree, operator, value):
    """
    Inputs:
        @ btree: the btree that corresponds to the attribute will be compared
        @ operator: Five operators supported: '<', '>', '=', '<=', '>=', '<>'
        @ value: Rvalue
    Return:
        @ return a two level list. Eg. [[1,2,3,4]], the row list for the single csv.
    """
    if isinstance(btree, str):
        btree = recoverFromPickle2(btree)
    if operator == '<':
        value_list = list(btree.values(min = btree.minKey(), max = value, excludemax=True))
    elif operator == '<=':
        value_list = list(btree.values(min = btree.minKey(), max = value))
    elif operator == '>':
        value_list = list(btree.values(min = value, max = btree.maxKey(), excludemin=True))
    elif operator == '>=':
        value_list = list(btree.values(min = value, max = btree.maxKey()))
    elif operator == '=':
        try:
            value_list =[btree[value]]
        except:
            value_list = []
    elif operator == '<>':
        ex_value_list = btree[value]
        all_value_list = list(btree.values())
        temp = []
        for i in range(len(all_value_list)):
            temp = temp + all_value_list[i]
        out = except_condition_single([temp]+[ex_value_list])
        return out
    else:
        print('invalid operator')
        value_list = []
    output = []
    for i in range(len(value_list)):
        output = output + value_list[i]
    # key_list = list(btree.keys())
    return [output]

# def single_join_filter_more(btree_list, operator_list, value_list):
    """
    Uncommend if necessary.
    """
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
    """
    Inputs:
        @ btree1: the btree that corresponds to the attribute in the first csv file that will be compared.
          Can be any comparable type.
        @ btree2: the btree that corresponds to the attribute in the second csv file that will be compared.
          Can be any comparable type.
        @ operator: Three operators supported: '<', '<=', '=', '<>' (Symmetric)
    Return:
        @ return a three level list. out = Eg. [[[1,2],[2,3]],[[1],[4,1,2]],...].
          Second level must be of length 2, which corresponds to the row for the first and second csv files.
          For the inner two level list, do a cartesian production between out[i][0] and out[i][1] to get the
          corresponding offset in the first and second file.
    """
    if isinstance(btree1, str):
        btree1 = recoverFromPickle2(btree1)
    if isinstance(btree2, str):
        btree2 = recoverFromPickle2(btree2)
    list1 = list(btree1.keys())
    list2 = list(btree2.keys())
    i = 0
    j = 0
    output = []
    if operator == '<':
        while (i <= len(list1) - 1 or j <= len(list2) - 1):
            if i == len(list1) - 1 and j == len(list2) - 1:
                if list1[i] < list2[j]:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                break
            elif i == len(list1) - 1:
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
        while (i <= len(list1) - 1 or j <= len(list2) - 1):
            if i == len(list1) - 1 and j == len(list2) - 1:
                if list1[i] <= list2[j]:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                break
            elif i == len(list1) - 1:
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
            if i == len(list1) - 1 and j == len(list2) - 1:
                if list1[i] == list2[j]:
                    output = output + [[list1[i], list2[j]]]
                break
            elif i == len(list1) - 1:
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
    if operator == '<>':
#        temp  = double_join_filter(btree2, btree1, '<')
#        temp1 = []
#        for i in range(len(temp)):
#            temp1 = [[temp[i][1]] + [temp[i][0]]] + temp1
        return double_join_filter(btree1, btree2, '<') 
    
#    return output
    row_list = [[btree1[item[0]], btree2[item[1]]] for item in output]
    return row_list
#    list_row = []
#    for i in range(len(row_list)):
#        list_row = list_row + list(itertools.product(row_list[i][0],row_list[i][1]))
#    list_row = [[item[0], item[1]] for item in list_row]
#    return list_row

def double_join_filter_plus(btree1, btree2, operator, value):
    """
    Inputs:
        @ btree1: the btree that corresponds to the attribute in the first csv file that will be compared.
          Can be any comparable type.
        @ btree2: the btree that corresponds to the attribute in the second csv file that will be compared.
          Can be any comparable type.
        @ operator: Three operators supported: '<', '<=', '=', '<>' (Symmetric)
    Return:
        @ return a three level list. out = Eg. [[[1,2],[2,3]],[[1],[4,1,2]],...].
          Second level must be of length 2, which corresponds to the row for the first and second csv files.
          For the inner two level list, do a cartesian production between out[i][0] and out[i][1] to get the
          corresponding offset in the first and second file.
    """
    if isinstance(btree1, str):
        btree1 = recoverFromPickle2(btree1)
    if isinstance(btree2, str):
        btree2 = recoverFromPickle2(btree2)
    list1 = list(btree1.keys())
    list2 = list(btree2.keys())
    i = 0
    j = 0
    output = []
    if operator == '<':
        while (i <= len(list1) - 1 or j <= len(list2) - 1):
            if i == len(list1) - 1 and j == len(list2) - 1:
                if list1[i] < list2[j] + value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                break
            elif i == len(list1) - 1:
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
        while (i <= len(list1) - 1 or j <= len(list2) - 1):
            if i == len(list1) - 1 and j == len(list2) - 1:
                if list1[i] <= list2[j] + value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                break
            elif i == len(list1) - 1:
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
            if i == len(list1) - 1 and j == len(list2) - 1:
                if list1[i] == list2[j] + value:
                    output = output + [[list1[i], list2[j]]]
                break
            elif i == len(list1) - 1:
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
                if list1[i] < list2[j] + value:
                    i += 1
                else: 
                    j += 1
    
    if operator == '<>':
        list2 = [item + value for item in output]
        output = except_condition_single([list1]+[list2])
        
#    return output
    row_list = [[btree1[item[0]], btree2[item[1]]] for item in output]
    return row_list
#    list_row = []
#    for i in range(len(row_list)):
#        list_row = list_row + list(itertools.product(row_list[i][0],row_list[i][1]))
#    list_row = [[item[0], item[1]] for item in list_row]
#    return list_row

def double_join_filter_multi(btree1, btree2, operator, value):
    """
    Inputs:
        @ btree1: the btree that corresponds to the attribute in the first csv file that will be compared.
          Must be double or int type.
        @ btree2: the btree that corresponds to the attribute in the second csv file that will be compared.
          Must be double or int type.
        @ operator: Three operators supported: '<', '<=', '=', '<>' (Symmetric)
        @ value: the value that will be multiplied to the right side of the equation.
    Return:
        @ return a two level list. Inner level must be of length 2, 
          which corresponds to the row for the first and second csv files. 
          Eg. [[1,2],[2,3],[1,4],...] not [[1,2,3],[4,5,6],...]    
    """
    if isinstance(btree1, str):
        btree1 = recoverFromPickle2(btree1)
    if isinstance(btree2, str):
        btree2 = recoverFromPickle2(btree2)
    list1 = list(btree1.keys())
    list2 = list(btree2.keys())
    i = 0
    j = 0
    output = []
    if operator == '<':
        while (i <= len(list1) - 1 or j <= len(list2) - 1):
            if i == len(list1) - 1 and j == len(list2) - 1:
                if list1[i] < list2[j] * value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                break
            elif i == len(list1) - 1:
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
        while (i <= len(list1) - 1 or j <= len(list2) - 1):
            if i == len(list1) - 1 and j == len(list2) - 1:
                if list1[i] <= list2[j] * value:
                    output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
                break
            elif i == len(list1) - 1:
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
            if i == len(list1) - 1 and j == len(list2) - 1:
                if list1[i] == list2[j] * value:
                    output = output + [[list1[i], list2[j]]]
                break
            elif i == len(list1) - 1:
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
                if list1[i] < list2[j] * value:
                    i += 1
                else: 
                    j += 1
    if operator == '<>':
        list2 = [item * value for item in output]
        output = except_condition_single([list1]+[list2])
#    return output
    row_list = [[btree1[item[0]], btree2[item[1]]] for item in output]
    return row_list
#    list_row = []
#    for i in range(len(row_list)):
#        list_row = list_row + list(itertools.product(row_list[i][0],row_list[i][1]))
#    list_row = [[item[0], item[1]] for item in list_row]
#    return list_row

def and_condition_single(list_row_list):
    """
    Inputs:
        @ list_row_list: list of different outputs from the above single join 
          function for one same csv different attributes. Eg: [[1,2,4,5],[4,5,7,8,9,11]]
          Need to change the two level list outputs of single join like [[1,2,4,5]] to a 
          single level list like [1,2,4,5] and combine to a two level list again. 
        @ Implement the AND condition for different row lists for the same csv file.
    Return:
        @ return a two level list the same as single join function. like [[4,5]]     
    """
    output = list_row_list[0]
    for i in range(len(list_row_list)):
        output = set(list_row_list[i]).intersection(output)
    return [list(output)]

def or_condition_single(list_row_list):
    """
    Inputs:
        @ list_row_list: list of different outputs from the above single join 
          function for one same csv different attributes. Eg: [[1,2,4,5],[4,5,7,8,9,11]]
          Need to change the two level list outputs of single join like [[1,2,4,5]] to a 
          single level list like [1,2,4,5] and combine to a two level list again. 
        @ Implement the OR condition for different row lists for the same csv file.
    Return:
        @ return a two level list the same as single join function. like [[4,5]]     
    """
    output = list_row_list[0]
    for i in range(len(list_row_list)):
        output = set(list_row_list[i]).union(output)
    return [list(output)]  

def except_condition_single(list_row_list):
    """
    Inputs:
        @ list_row_list: list of different outputs from the above single join 
          function for one same csv different attributes. Eg: [[1,2,4,5],[4,5,7,8,9,11]]
          Need to change the two level list outputs of single join like [[1,2,4,5]] to a 
          single level list like [1,2,4,5] and combine to a two level list again. 
        @ Implement the OR condition for different row lists for the same csv file.
        @ The length of the list_row_list must be two. Item[0] except item[1].
    Return:
        @ return a two level list the same as single join function. like [[4,5]]     
    """
    output = set(list_row_list[0]).difference(list_row_list[1])
    return [list(output)]  

def and_condition_double(list_row_list1, list_row_list2, id1, id2):
    """
    Inputs:
        @ list_row_list1: output from the above double join functions or from this function.
          Eg.:[[1,3],[2,5],[5,6]](orginal output from double join functions) 
              or [[1,3,5], [4,6,7], [2,5,6]] (after one double join, the output from this function). 
        @ list_row_list2: Can only be the output from the above double join functions.
          Eg.:[[1,3],[2,5],[5,6]](orginal output from double join functions) 
        @ list_row_list1 and list_row_list2 share the same attribute from the same csv file 
          at the first value of each item. And the other attributes should be different attribute
          from different csv files.
          Eg.: [[1,3,5], [4,6,7], [2,5,6]]
                 |        |        |
               [[1,3],   [4,5],   [2,6]]
    Return:
        @ return similar output as double join functions, two level list but the inner level not
          necessary to be of length 2. 
        @ Each item in output should be the same length list. 
          Eg.:[[1,2,3,4],[1,3,4,5],[5,6,7,9]] corresponding to 4 different csv files A,B,C,D
    """
    output = []
    for i in range(len(list_row_list1)):
        for j in range(len(list_row_list2)):
            if list_row_list1[i][id1] == list_row_list2[j][id2]:
                temp = list_row_list1[i] + [list_row_list2[j][1-id2]]
                output.append(temp)
    return output

def permute_list(list_row_list):
    """
    Inputs:
        @ list_row_list: output from the above double join functions or from and_condition_double function.
          Eg.:[[1,3],[2,5],[5,6]](orginal output from double join functions) 
              or [[1,3,5], [4,6,7]] (after one double join, the output from and_condition_double function).
        @ [[1,3,5], [4,6,7]] corresponding to three different csv files.
    Return:
        @ return a two level list that each item corresponds to one csv file. Like the permute operator in matrix.
    
    @ Eg. Input: [[1,2,4], [2,6,5]]
          Output: [[1,2], [2,6], [4,5]] --- Each item is for one csv file. 
                                            
    """
    output = []
    if len(list_row_list) == 0:
        return output
    for i in range(len(list_row_list[0])):
        temp = []
        for j in range(len(list_row_list)):
            temp = temp + [list_row_list[j][i]]
        output = output + [temp]
    return output

def single_to_double(list_row):
    """
    
    """
    output = []
    for i in range(len(list_row[0])):
        output = output + [[list_row[0][i]]]
    return output

def cross_prod(row_list):
    """
    Inputs:
        @ row_list: A three level list: Eg.: [[[1,2],[2,3]],[[1],[4,1,2]],...]
    Return:
        @ return a two level list after doing a cartesian production between each item (two level list)
          in the original three level list. Eg. [[1, 2], [1, 3], [2, 2], [2, 3], [1, 4], [1, 1], [1, 2]]
     """
#    row_list = [[btree1[item[0]], btree2[item[1]]] for item in output]
    
    list_row = []
    for i in range(len(row_list)):
        list_row = list_row + list(itertools.product(row_list[i][0],row_list[i][1]))
    list_row = [[item[0], item[1]] for item in list_row]
    return list_row

def A_AB_B_and(A, AB, B):
    """
    This is a filter function to shrink the join result before cartesian production
    Inputs:
        @ A: a two level list which can be the output from single_join_filter_one,
          and_condition_single, or_condition_single and except_condition_single.
          Eg.: [[2,3,4,5,6]]
        @ B: Same as A
        @ AB: a three level list which can be the output from double_join_filter function sets
          and other filter function. A and B should at the corresponding location, which means
          the input should be like A_AB_B(A, AB, B) or A_AB_B(B, BA, A).
    Return:
        @ The same structure as input AB, in order to make the filter operation a closure.
          The sequence of the corresponding csv files is still AB'.
    """
    output = []
    for i in range(len(AB)):
        temp1 = and_condition_single([AB[i][0]] + A)
        temp2 = and_condition_single([AB[i][1]] + B)
        if len(temp1[0]) != 0 and len(temp2[0]) != 0:
            output = output + [temp1+temp2]
    return output

def A_AB_and(A, AB, id):
    """
    This is a filter function to shrink the join result before cartesian production
    Inputs:
        @ A: a two level list which can be the output from single_join_filter_one,
          and_condition_single, or_condition_single and except_condition_single.
          Eg.: [[2,3,4,5,6]]
        @ AB: a three level list which can be the output from double_join_filter function sets
          and other filter function.
        @ id: the order of the input file, if the input file is (AB and A) or (BA and B), id should
          be 0, otherwise 1.
    Return:
        @ The same structure as input AB, in order to make the filter operation a closure.
          The sequence of the corresponding csv files is still AB'.
    """
    output = []
    for i in range(len(AB)):
#        print([AB[i][id]] + A)
        temp1 = and_condition_single([AB[i][id]] + A)
        temp2 = [AB[i][1-id]]
        if len(temp1[0]) != 0 and len(temp2[0]) != 0:
            if id == 0:           
                output = output + [temp1+temp2]
            else:
                output = output + [temp2+temp1]
    return output


def A_AB_B_or(A, AB, B):
    """
    This is a filter function to shrink the join result before cartesian production
    Inputs:
        @ A: a two level list which can be the output from single_join_filter_one,
          and_condition_single, or_condition_single and except_condition_single.
          Eg.: [[2,3,4,5,6]]
        @ B: Same as A
        @ AB: a three level list which can be the output from double_join_filter function sets
          and other filter function. A and B should at the corresponding location, which means
          the input should be like A_AB_B(A, AB, B) or A_AB_B(B, BA, A).
    Return:
        @ The same structure as input AB, in order to make the filter operation a closure.
          The sequence of the corresponding csv files is still AB'.
    """
    output = []
    for i in range(len(AB)):
        temp1 = or_condition_single([AB[i][0]] + A)
        temp2 = or_condition_single([AB[i][1]] + B)
        if len(temp1[0]) != 0 and len(temp2[0]) != 0:
            output = output + [temp1+temp2]
    return output

def AB_AB(AB1, AB2, id):
    """
    This is NOT a filter function. This is a join function which will only return one result.
    Inputs:
        @ AB1: a two level list which can only be the cross_prod and AB_AB output.
          Eg.: [[1, 2], [1, 3], [2, 2], [2, 3], [1, 4], [1, 1], [1, 2]]
        @ AB2: same as AB1
        @ id: imply the order of the two inputs. Select to be 0 if they are same, otherwise 1.
    Return:
        @ A two level list
    """
    if id == 0:       
        A = [(item[0], item[1]) for item in AB1]
        B = [(item[0], item[1]) for item in AB2]
    if id == 1:
        A = [(item[0], item[1]) for item in AB1]
        B = [(item[1], item[0]) for item in AB2]        
    out = and_condition_single([A] + [B])[0]
    output = [[item[0], item[1]] for item in out]
    return output


def AB_AB_or(AB1, AB2, id):
    """
    This is a filter function to shrink the join result before cartesian production
    Inputs:
        @ A: a two level list which can be the output from single_join_filter_one,
          and_condition_single, or_condition_single and except_condition_single.
          Eg.: [[2,3,4,5,6]]
        @ AB: a three level list which can be the output from double_join_filter function sets
          and other filter function.
        @ id: the order of the input file, if the input file is (AB and A) or (BA and B), id should
          be 0, otherwise 1.
    Return:
        @ The same structure as input AB, in order to make the filter operation a closure.
          The sequence of the corresponding csv files is still AB'.
    """
    if id == 0:
        A = [(item[0], item[1]) for item in AB1]
        B = [(item[0], item[1]) for item in AB2]
    if id == 1:
        A = [(item[0], item[1]) for item in AB1]
        B = [(item[1], item[0]) for item in AB2]
    out = or_condition_single([A] + [B])[0]
    output = [[item[0], item[1]] for item in out]
    return output

def AB_AC(AB, AC, id1, id2):
    """
    This is a filter function to shrink the join result before cartesian production
    Inputs:
        @ AB: a three level list which can be the output from double_join_filter function sets
          and other filter function. The order is AB.
        @ AC: a three level list which can be the output from double_join_filter function sets
          and other filter function.   The order is AC.
        @ id1: the location of the common attribute in AB input.
        @ id2: the location of the common attribute in AC input.
        If the input is (AB and AC), id1 and id2 should be (0, 0).
    Return:
        @ The same structure as input AB and AC, in order to make the filter operation a closure.
          The sequence of the corresponding csv files is still AB' and AC'.
    """
    temp = []
    for i in range(len(AB)):
        temp = or_condition_single([AB[i][id1]] + temp)
    AB_new = A_AB_and(temp, AB, id1)
    tem = []
    for j in range(len(AC)):
        tem = or_condition_single([AC[j][id2]] + tem)
    AC_new = A_AB_and(tem, AC, id2)
    return [AB_new, AC_new]

def A_a_B_b_file(path1, offsetlist1, attr1, path2, offsetlist2, attr2, operator, isNumber):
    """
    This is a funtion which will touch two csv files directly. File1 must be the small (filtered) one.
    Inputs:
        @ path1: the path to reach the first csv file.
        @ path2: the path to reach the second csv file.
        @ offsetlist1: a two level list which corresponds to the filtered offsets in the first csv file.
        @ offsetlist2: a two level list which corresponds to the filtered offsets in the second csv file.
        @ attr1: the index for the common attribute in the first csv file.
        @ attr2: the index for the common attribute in the second csv file.
        @ operator: Five operators supported: '<', '>', '=', '<=', '>=', '<>'
        @ isNumber: the common attribute is number or not.
    Return:
        @ A three level list with the same sturcture and meaning as the output from the all the filter functions.
    """
    out = []
    with open(path1, 'r', encoding="ISO-8859-1") as file1:
        with open(path2, 'r', encoding="ISO-8859-1") as file2:
            f1 = csv.reader(file1)
            f2 = csv.reader(file2)
            for i in range(len(offsetlist1[0])):
                temp1 = [offsetlist1[0][i]]
                temp2 = []
                for j in range(len(offsetlist2[0])):
                    file1.seek(0)
                    file2.seek(0)
                    file1.seek(offsetlist1[0][i])
                    file2.seek(offsetlist2[0][j])
                    row1 = next(f1)
                    row2 = next(f2)
                    if isNumber:
                        if operator == '=' and float(row1[attr1]) == float(row2[attr2]):
                            temp2 = temp2 + [offsetlist2[0][j]]
                        elif operator == '<' and float(row1[attr1]) < float(row2[attr2]):
                            temp2 = temp2 + [offsetlist2[0][j]]
                        elif operator == '<=' and float(row1[attr1]) <= float(row2[attr2]):
                            temp2 = temp2 + [offsetlist2[0][j]]
                        elif operator == '>' and float(row1[attr1]) > float(row2[attr2]):
                            temp2 = temp2 + [offsetlist2[0][j]]
                        elif operator == '>=' and float(row1[attr1]) >= float(row2[attr2]):
                            temp2 = temp2 + [offsetlist2[0][j]]
                        elif operator == '<>' and float(row1[attr1]) != float(row2[attr2]):
                            temp2 = temp2 + [offsetlist2[0][j]]
                    else:
                        if operator == '=' and row1[attr1].upper() == row2[attr2].upper():
                            temp2 = temp2 + [offsetlist2[0][j]]
                        elif operator == '<' and row1[attr1].upper() < row2[attr2].upper():
                            temp2 = temp2 + [offsetlist2[0][j]]
                        elif operator == '<=' and row1[attr1].upper() <= row2[attr2].upper():
                            temp2 = temp2 + [offsetlist2[0][j]]
                        elif operator == '>' and row1[attr1].upper() > row2[attr2].upper():
                            temp2 = temp2 + [offsetlist2[0][j]]
                        elif operator == '>=' and row1[attr1].upper() >= row2[attr2].upper():
                            temp2 = temp2 + [offsetlist2[0][j]]
                        elif operator == '<>' and row1[attr1].upper() != row2[attr2].upper():
                            temp2 = temp2 + [offsetlist2[0][j]]
                if len(temp2) > 0:
                    temp = [temp1] + [temp2]
                    out = out + [temp]
    return out

def A_a_B_b_file_plus(path1, offsetlist1, attr1, path2, offsetlist2, attr2, operator, value):
    """
    This is a funtion which will touch two csv files directly. File1 must be the small (filtered) one.
    Inputs:
        @ path1: the path to reach the first csv file.
        @ path2: the path to reach the second csv file.
        @ offsetlist1: a two level list which corresponds to the filtered offsets in the first csv file.
        @ offsetlist2: a two level list which corresponds to the filtered offsets in the second csv file.
        @ attr1: the index for the common attribute in the first csv file.
        @ attr2: the index for the common attribute in the second csv file.
        @ operator: Five operators supported: '<', '>', '=', '<=', '>=', '<>'
        @ value: the value that will be added on the right handside.
    Return:
        @ A three level list with the same sturcture and meaning as the output from the all the filter functions.
    """
    out = []
    with open(path1, 'r', encoding="ISO-8859-1") as file1:
        with open(path2, 'r', encoding="ISO-8859-1") as file2:
            f1 = csv.reader(file1)
            f2 = csv.reader(file2)
            for i in range(len(offsetlist1[0])):
                temp1 = [offsetlist1[0][i]]
                temp2 = []
                for j in range(len(offsetlist2[0])):
                    file1.seek(0)
                    file2.seek(0)
                    file1.seek(offsetlist1[0][i])
                    file2.seek(offsetlist2[0][j])
                    row1 = next(f1)
                    row2 = next(f2)
                    if operator == '=' and float(row1[attr1]) == float(row2[attr2]) + value:
                        temp2 = temp2 + [offsetlist2[0][j]]
                    elif operator == '<' and float(row1[attr1]) < float(row2[attr2]) + value:
                        temp2 = temp2 + [offsetlist2[0][j]]
                    elif operator == '<=' and float(row1[attr1]) <= float(row2[attr2]) + value:
                        temp2 = temp2 + [offsetlist2[0][j]]
                    elif operator == '>' and float(row1[attr1]) > float(row2[attr2]) + value:
                        temp2 = temp2 + [offsetlist2[0][j]]
                    elif operator == '>=' and float(row1[attr1]) >= float(row2[attr2]) + value:
                        temp2 = temp2 + [offsetlist2[0][j]]
                    elif operator == '<>' and float(row1[attr1]) != float(row2[attr2]) + value:
                        temp2 = temp2 + [offsetlist2[0][j]]
                if len(temp2) > 0:
                    temp = [temp1] + [temp2]
                    out = out + [temp]
    return out    

def A_a_B_b_file_multi(path1, offsetlist1, attr1, path2, offsetlist2, attr2, operator, value):
    """
    This is a funtion which will touch two csv files directly. File1 must be the small (filtered) one.
    Inputs:
        @ path1: the path to reach the first csv file.
        @ path2: the path to reach the second csv file.
        @ offsetlist1: a two level list which corresponds to the filtered offsets in the first csv file.
        @ offsetlist2: a two level list which corresponds to the filtered offsets in the second csv file.
        @ attr1: the index for the common attribute in the first csv file.
        @ attr2: the index for the common attribute in the second csv file.
        @ operator: Five operators supported: '<', '>', '=', '<=', '>=', '<>'
        @ value: the value that will be multiplied on the right handside.
    Return:
        @ A three level list with the same sturcture and meaning as the output from the all the filter functions.
    """
    out = []
    with open(path1, 'r', encoding="ISO-8859-1") as file1:
        with open(path2, 'r', encoding="ISO-8859-1") as file2:
            f1 = csv.reader(file1)
            f2 = csv.reader(file2)
            for i in range(len(offsetlist1[0])):
                temp1 = [offsetlist1[0][i]]
                temp2 = []
                for j in range(len(offsetlist2[0])):
                    file1.seek(0)
                    file2.seek(0)
                    file1.seek(offsetlist1[0][i])
                    file2.seek(offsetlist2[0][j])
                    row1 = next(f1)
                    row2 = next(f2)
                    if operator == '=' and float(row1[attr1]) == float(row2[attr2]) * value:
                        temp2 = temp2 + [offsetlist2[0][j]]
                    elif operator == '<' and float(row1[attr1]) < float(row2[attr2]) * value:
                        temp2 = temp2 + [offsetlist2[0][j]]
                    elif operator == '<=' and float(row1[attr1]) <= float(row2[attr2]) * value:
                        temp2 = temp2 + [offsetlist2[0][j]]
                    elif operator == '>' and float(row1[attr1]) > float(row2[attr2]) * value:
                        temp2 = temp2 + [offsetlist2[0][j]]
                    elif operator == '>=' and float(row1[attr1]) >= float(row2[attr2]) * value:
                        temp2 = temp2 + [offsetlist2[0][j]]
                    elif operator == '<>' and float(row1[attr1]) != float(row2[attr2]) * value:
                        temp2 = temp2 + [offsetlist2[0][j]]
                if len(temp2) > 0:
                    temp = [temp1] + [temp2]
                    out = out + [temp]
    return out

def btree_A_a_file(btree, path, offsetlist, attr, operator, isNumber):
    """
    This is a funtion which will touch the second csv file directly.
    Inputs:
        @ btree: the LHS input. A btree file.
        @ path: the path to reach the second csv file.
        @ offsetlist: a two level list which corresponds to the filtered offsets in the second csv file.
        @ attr: the index for the common attribute in the second csv file.
        @ operator: Five operators supported: '<', '>', '=', '<=', '>=', '<>'
        @ isNumber: the common attribute is number or not.
    Return:
        @ A three level list with the same sturcture and meaning as the output from the all the filter functions.
    """
    if isinstance(btree, str):
        btree = recoverFromPickle2(btree)
    out = []
    with open(path, 'r', encoding="ISO-8859-1") as file:
        f = csv.reader(file)
        for i in range(len(offsetlist[0])):
            file.seek(0)
            file.seek(offsetlist[0][i])
            row = next(f)
            temp1 = [offsetlist[0][i]]
            if isNumber:
                value = float(row[attr])
            else:
                value = row[attr].upper()
            temp2 = single_join_filter_one(btree, operator, value)
#            print(temp2)
            if len(temp2[0]) > 0:
                temp = temp2 + [temp1]
                out = out + [temp]
    return out

def btree_A_a_file_plus(btree, path, offsetlist, attr, operator, val):
    """
    This is a funtion which will touch the second csv file directly.
    Inputs:
        @ btree: the LHS input. A btree file.
        @ path: the path to reach the second csv file.
        @ offsetlist: a two level list which corresponds to the filtered offsets in the second csv file.
        @ attr: the index for the common attribute in the second csv file.
        @ operator: Five operators supported: '<', '>', '=', '<=', '>=', '<>'
        @ val: the value that will be added on the right handside.
    Return:
        @ A three level list with the same sturcture and meaning as the output from the all the filter functions.
    """
    if isinstance(btree, str):
        btree = recoverFromPickle2(btree)
    out = []
    with open(path, 'r', encoding="ISO-8859-1") as file:
        f = csv.reader(file)
        for i in range(len(offsetlist[0])):
            file.seek(0)
            file.seek(offsetlist[0][i])
            row = next(f)
            temp1 = [offsetlist[0][i]]
            value = float(row[attr]) + val
            temp2 = single_join_filter_one(btree, operator, value)
#            print(temp2)
            if len(temp2[0]) > 0:
                temp = temp2 + [temp1]
                out = out + [temp]
    return out

def btree_A_a_file_multi(btree, path, offsetlist, attr, operator, val):
    """
    This is a funtion which will touch the second csv file directly.
    Inputs:
        @ btree: the LHS input. A btree file.
        @ path: the path to reach the second csv file.
        @ offsetlist: a two level list which corresponds to the filtered offsets in the second csv file.
        @ attr: the index for the common attribute in the second csv file.
        @ operator: Five operators supported: '<', '>', '=', '<=', '>=', '<>'
        @ val: the value that will be multiplied on the right handside.
    Return:
        @ A three level list with the same sturcture and meaning as the output from the all the filter functions.
    """
    if isinstance(btree, str):
        btree = recoverFromPickle2(btree)
    out = []
    with open(path, 'r', encoding="ISO-8859-1") as file:
        f = csv.reader(file)
        for i in range(len(offsetlist[0])):
            file.seek(0)
            file.seek(offsetlist[0][i])
            row = next(f)
            temp1 = [offsetlist[0][i]]
            value = float(row[attr]) * val
            temp2 = single_join_filter_one(btree, operator, value)
#            print(temp2)
            if len(temp2[0]) > 0:
                temp = temp2 + [temp1]
                out = out + [temp]
    return out

def A_a_btree_file(path, offsetlist, attr, btree, operator, isNumber):
    """
    This is a funtion which will touch the first csv file directly.
    Inputs:
        @ btree: the LHS input. A btree file.
        @ path: the path to reach the first csv file.
        @ offsetlist: a two level list which corresponds to the filtered offsets in the first csv file.
        @ attr: the index for the common attribute in the second csv file.
        @ operator: Five operators supported: '<', '>', '=', '<=', '>=', '<>'
        @ isNumber: the common attribute is number or not.
    Return:
        @ A three level list with the same sturcture and meaning as the output from the all the filter functions.
    """
    if isinstance(btree, str):
        btree = recoverFromPickle2(btree)
    out = []
    with open(path, 'r', encoding="ISO-8859-1") as file:
        f = csv.reader(file)
        for i in range(len(offsetlist[0])):
            file.seek(0)
            file.seek(offsetlist[0][i])
            row = next(f)
            temp1 = [offsetlist[0][i]]
            if isNumber:
                value = float(row[attr])
            else:
                value = row[attr].upper()
            if operator == '<':
                op = '>'
            elif operator == '<=':
                op = '>='
            elif operator == '>':
                op = '<'
            elif operator == '>=':
                op = '<='
            else:
                op = operator
            temp2 = single_join_filter_one(btree, op, value)
#            print(len(temp2[0]))
            if len(temp2[0]) > 0 and len(temp1) > 0:
                temp = [temp1] + temp2
                out = out + [temp]
    return out

def A_a_btree_file_plus(path, offsetlist, attr, btree, operator, val):
    """
    This is a funtion which will touch the first csv file directly.
    Inputs:
        @ btree: the LHS input. A btree file.
        @ path: the path to reach the first csv file.
        @ offsetlist: a two level list which corresponds to the filtered offsets in the first csv file.
        @ attr: the index for the common attribute in the second csv file.
        @ operator: Five operators supported: '<', '>', '=', '<=', '>=', '<>'
        @ val: the value that will be added on the right handside.
    Return:
        @ A three level list with the same sturcture and meaning as the output from the all the filter functions.
    """
    if isinstance(btree, str):
        btree = recoverFromPickle2(btree)
    out = []
    with open(path, 'r', encoding="ISO-8859-1") as file:
        f = csv.reader(file)
        for i in range(len(offsetlist[0])):
            file.seek(0)
            file.seek(offsetlist[0][i])
            row = next(f)
            temp1 = [offsetlist[0][i]]
            value = float(row[attr]) + val
            if operator == '<':
                op = '>'
            elif operator == '<=':
                op = '>='
            elif operator == '>':
                op = '<'
            elif operator == '>=':
                op = '<='
            else:
                op = operator
            temp2 = single_join_filter_one(btree, op, value)
#            print(len(temp2[0]))
            if len(temp2[0]) > 0 and len(temp1) > 0:
                temp = [temp1] + temp2
                out = out + [temp]
    return out

def A_a_btree_file_multi(path, offsetlist, attr, btree, operator, val):
    """
    This is a funtion which will touch the first csv file directly.
    Inputs:
        @ btree: the LHS input. A btree file.
        @ path: the path to reach the first csv file.
        @ offsetlist: a two level list which corresponds to the filtered offsets in the first csv file.
        @ attr: the index for the common attribute in the second csv file.
        @ operator: Five operators supported: '<', '>', '=', '<=', '>=', '<>'
        @ val: the value that will be multiplied on the right handside.
    Return:
        @ A three level list with the same sturcture and meaning as the output from the all the filter functions.
    """
    if isinstance(btree, str):
        btree = recoverFromPickle2(btree)
    out = []
    with open(path, 'r', encoding="ISO-8859-1") as file:
        f = csv.reader(file)
        for i in range(len(offsetlist[0])):
            file.seek(0)
            file.seek(offsetlist[0][i])
            row = next(f)
            temp1 = [offsetlist[0][i]]
            value = float(row[attr]) * val
            if operator == '<':
                op = '>'
            elif operator == '<=':
                op = '>='
            elif operator == '>':
                op = '<'
            elif operator == '>=':
                op = '<='
            else:
                op = operator
            temp2 = single_join_filter_one(btree, op, value)
#            print(len(temp2[0]))
            if len(temp2[0]) > 0 and len(temp1) > 0:
                temp = [temp1] + temp2
                out = out + [temp]
    return out

def get_small_btree(path, offsetlist, attr, isNumber):
    """
    This is a funtion that will rebuild a smaller btree for the given attribute ID and offsetlist.
    Input:
        @ path: the path to reach the related csv file.
        @ offsetlist: a two level list which contains all the filtered offsets in csv file.
        @ attr: the index for the corresponding attribute.
        @ isNumber: the corresponding attribute is number or not.
    """
    dict = {}
    with open(path, 'r', encoding="ISO-8859-1") as file:
        f = csv.reader(file)
        for i in range(len(offsetlist[0])):
            file.seek(0)
            file.seek(offsetlist[0][i])
            row = next(f)
            # print(row[1])
            if isNumber:
                try:
                    key = float(row[attr])
                except:
                    key = 0.0
            else:
                key = row[attr].upper()
            if key in dict:
                dict[key].append(offsetlist[0][i])
            else:
                # create a list that store the row index w.r.t the tuple
                dict[key] = [offsetlist[0][i]]
    sys.setrecursionlimit(1000)
    t = OOBTree()
    t.update(dict)
    return t

def get_A_B_AB_and(list):
    """
    This is a function that will squeeze AB and get the independent offsetlists for A and B under and condition.
    Input:
        @ list: a three level list. Eg.: [[[1,2],[2,3]],[[1],[4,1,2]]]
    Return:
        @ two of two level list, sequence is the same as input AB. Eg.: ([[1]], [[2]])
    """
    temp1 = []
    temp2 = []
    for i in range(len(list)):
        temp1 = temp1 + [list[i][0]]
        temp2 = temp2 + [list[i][1]]
    return and_condition_single(temp1), and_condition_single(temp2)

def get_A_B_AB_or(list):
    """
    This is a function that will squeeze AB and get the independent offsetlists for A and B under or condition.
    Input:
        @ list: a three level list. Eg.: [[[1,2],[2,3]],[[1],[4,1,2]]]
    Return:
        @ two of two level list, sequence is the same as input AB. Eg.: ([[1, 2]], [[1, 2, 3, 4]])
    """
    temp1 = []
    temp2 = []
    for i in range(len(list)):
        temp1 = temp1 + [list[i][0]]
        temp2 = temp2 + [list[i][1]]
    return or_condition_single(temp1), or_condition_single(temp2)


# def excep(AB, out):
#     """
#     This is a function that will handle the complex unequality condition between two csv files,
#     not just one csv file and a value.
#     Input:
#         @ AB: a three level list after all the other conditions and filters.
#         @ out: the corresponding output for the same A,B files but under equal condition which is
#           what we want to get rid of from the input AB.
#     Return:
#         @ a three level list, the same as the input AB considering the sturcture, meaning and sequence.
#
#     """
#     idx = []
#     AB_new = copy.deepcopy(AB)
#     for i in range(len(out)):
#         for j in range(len(AB_new)):
#             if len(set(out[i][0]).intersection(AB_new[j][0])) > 0:
#                 #            if out[i][0][0] in AB[j][0]:
#                 temp = except_condition_single([AB_new[j][1]] + [out[i][1]])[0]
#                 if len(temp) != 0:
#                     #                    print('i: ',i)
#                     #                    print('j: ',j)
#                     #                    print([AB[j][1]] + [out[i][1]])
#                     #                    print(temp)
#                     #                    print('-------------')
#                     AB_new[j][1] = temp
#                 # print('new: ', AB_new)
#                 elif len(temp) == 0:
#                     if j not in idx:
#                         idx += [j]
#     temp1 = copy.deepcopy(AB_new)
#     for i in idx:
#         AB_new.remove(temp1[i])
#     # print(len(AB_new))
#
#     return AB_new



#def AB_AB_and(AB1, AB2):
#    """
#    
#    """
#    if len(AB1 > AB2):
#        a = AB2
#        b = AB1
#    else:
#        a = AB1
#        b = AB2
#    for i in range(len(a)):
#        for j in range(len(a[0][0])):
#            for k in range(len(b)):
#                if a[i][j] in 


"""
list1 = list(btree_a2.keys())#[1,2,3,5,9,10,11,14,23]
list2 = list(btree_a1.keys())#[1,2,3,5,9,10,11,14,23]
i = 0
j = 0
output = []
operator = '<'
if operator == '<':    
    while (i <= len(list1) - 1 or j <= len(list2) - 1):
        if i == len(list1) - 1 and j == len(list2) - 1:
            if list1[i] < list2[j]:
                output = output + list(list(itertools.product([list1[i]], list2[j:len(list2)])))
            break
        elif i == len(list1) - 1:
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
row_list = [[btree_a2[item[0]], btree_a1[item[1]]] for item in output]

list_row = []
for i in range(len(row_list)):
    list_row = list_row + list(itertools.product(row_list[i][0],row_list[i][1]))
list_row = [[item[0], item[1]] for item in list_row]
    
#double_join_filter(btree_a2,btree_a1,'<')        
"""














