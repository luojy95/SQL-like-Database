import itertools
from myCSV import *
from mybtree import *
    
def single_join_filter_one(btree, operator, value):
    '''
    Inputs:
        @ btree: the btree that corresponds to the attribute will be compared
        @ operator: Five operators supported: '<', '>', '=', '<=', '>=', '<>'
        @ value: Rvalue
    Return:
        @ return a two level list. Eg. [[1,2,3,4]], the row list for the single csv.
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
        value_list = [btree[value]]
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
    '''
    Uncommend if necessary.
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
    Inputs:
        @ btree1: the btree that corresponds to the attribute in the first csv file that will be compared.
          Can be any comparable type.
        @ btree2: the btree that corresponds to the attribute in the second csv file that will be compared.
          Can be any comparable type.
        @ operator: Three operators supported: '<', '<=', '=', '<>' (Symmetric)
    Return:
        @ return a two level list. Inner level must be of length 2, 
          which corresponds to the row for the first and second csv files. 
          Eg. [[1,2],[2,3],[1,4],...] not [[1,2,3],[4,5,6],...]  
    '''
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
        output = except_condition_single([list1]+[list2])
    else:
        print('invalid operator')
        return []
    
    row_list = [[btree1[item[0]], btree2[item[1]]] for item in output]
    
    list_row = []
    for i in range(len(row_list)):
        list_row = list_row + list(itertools.product(row_list[i][0],row_list[i][1]))
    list_row = [[item[0], item[1]] for item in list_row]
    return list_row

def double_join_filter_plus(btree1, btree2, operator, value):
    '''
    Inputs:
        @ btree1: the btree that corresponds to the attribute in the first csv file that will be compared.
          Must be double or int type.
        @ btree2: the btree that corresponds to the attribute in the second csv file that will be compared.
          Must be double or int type.
        @ operator: Three operators supported: '<', '<=', '=', '<>' (Symmetric)
        @ value: the value that will be added to the right side of the equation.
    Return:
        @ return a two level list. Inner level must be of length 2, 
          which corresponds to the row for the first and second csv files. 
          Eg. [[1,2],[2,3],[1,4],...] not [[1,2,3],[4,5,6],...]   
    '''
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
        
    else:
        print('invalid operator')
        return []    
    row_list = [[btree1[item[0]], btree2[item[1]]] for item in output]
    
    list_row = []
    for i in range(len(row_list)):
        list_row = list_row + list(itertools.product(row_list[i][0],row_list[i][1]))
    list_row = [[item[0], item[1]] for item in list_row]
    return list_row


def double_join_filter_multi(btree1, btree2, operator, value):
    '''
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
    '''
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
    else:
        print('invalid operator')
        return []
    
    row_list = [[btree1[item[0]], btree2[item[1]]] for item in output]
    
    list_row = []
    for i in range(len(row_list)):
        list_row = list_row + list(itertools.product(row_list[i][0],row_list[i][1]))
    list_row = [[item[0], item[1]] for item in list_row]
    return list_row

def and_condition_single(list_row_list):
    '''
    Inputs:
        @ list_row_list: list of different outputs from the above single join 
          function for one same csv different attributes. Eg: [[1,2,4,5],[4,5,7,8,9,11]]
          Need to change the two level list outputs of single join like [[1,2,4,5]] to a 
          single level list like [1,2,4,5] and combine to a two level list again. 
        @ Implement the AND condition for different row lists for the same csv file.
    Return:
        @ return a two level list the same as single join function. like [[4,5]]     
    '''
    output = list_row_list[0]
    for i in range(len(list_row_list)):
        output = set(list_row_list[i]).intersection(output)
    return [list(output)]

def or_condition_single(list_row_list):
    '''
    Inputs:
        @ list_row_list: list of different outputs from the above single join 
          function for one same csv different attributes. Eg: [[1,2,4,5],[4,5,7,8,9,11]]
          Need to change the two level list outputs of single join like [[1,2,4,5]] to a 
          single level list like [1,2,4,5] and combine to a two level list again. 
        @ Implement the OR condition for different row lists for the same csv file.
    Return:
        @ return a two level list the same as single join function. like [[4,5]]     
    '''
    output = list_row_list[0]
    for i in range(len(list_row_list)):
        output = set(list_row_list[i]).union(output)
    return [list(output)]  

def except_condition_single(list_row_list):
    '''
    Inputs:
        @ list_row_list: list of different outputs from the above single join 
          function for one same csv different attributes. Eg: [[1,2,4,5],[4,5,7,8,9,11]]
          Need to change the two level list outputs of single join like [[1,2,4,5]] to a 
          single level list like [1,2,4,5] and combine to a two level list again. 
        @ Implement the OR condition for different row lists for the same csv file.
        @ The length of the list_row_list must be two. Item[0] except item[1].
    Return:
        @ return a two level list the same as single join function. like [[4,5]]     
    '''
    output = set(list_row_list[0]).difference(list_row_list[1])
    return [list(output)]  

def and_condition_double(list_row_list1, list_row_list2, id1, id2):
    '''
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
    '''
    output = []
    for i in range(len(list_row_list1)):
        for j in range(len(list_row_list2)):
            if list_row_list1[i][id1] == list_row_list2[j][id2]:
                temp = list_row_list1[i] + [list_row_list2[j][1-id2]]
                output.append(temp)
    return output

def permute_list(list_row_list):
    '''
    Inputs:
        @ list_row_list: output from the above double join functions or from and_condition_double function.
          Eg.:[[1,3],[2,5],[5,6]](orginal output from double join functions) 
              or [[1,3,5], [4,6,7]] (after one double join, the output from and_condition_double function).
        @ [[1,3,5], [4,6,7]] corresponding to three different csv files.
    Return:
        @ return a two level list that each item corresponds to one csv file. Like the permute operator in matrix.
    
    @ Eg. Input: [[1,2,4], [2,6,5]]
          Output: [[1,2], [2,6], [4,5]] --- Each item is for one csv file. 
                                            
    '''
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
    '''
    
    '''
    output = []
    for i in range(len(list_row[0])):
        output = output + [[list_row[0][i]]]
    return output


list1 = [1,2,3,5,9,10,11,14,23]
list2 = [2,4,6,9,10,14]
i = 0
j = 0
output = []
operator = '='
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
    
        












