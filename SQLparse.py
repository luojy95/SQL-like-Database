import sqlparse
from myCSV import *
import ntpath
from join import *
from select_and_print import ProjectAndPrint
import time
import csv

class Sql_parsing(object):
    """
    This class is built to parse SQL input, optimize query and output query result.
    """
    def __init__(self, sql, indexpath):
        """
        This funciton build the object with SQL input and Btree file path and print out query result with
        Args:
            sql(string): SQL input in the terminal
            indexpath(string): path to store the btree file
            self.alias_dic: a dictionary that stores the relation of csv file and their alias
        Returns:
            print out query results and count time consuming
         """
        self.opt = 5000
        self.sql = sql
        self.parsed = sqlparse.parse(sql)
        self.token_list = self.parsed[0].tokens
        self.alias_dic = {}
        start = time.time()
        csv_list, alias_colume = self.PairCsvandAlias()
        self.indexpath = indexpath
        union = self.Whereparse()
        result = self.getQueryresult(union)
        query_time = time.time() - start
        ProjectAndPrint(self.sql, result[0],result[1])
        print(query_time)

    # the function the parse the SELECT part (before FROM) with sql statement as the input.
    # If the SELECT is not *, the outpub is a list of alias (can be None is no alias provided)
    # and a list of the corresponding attribute.
    # If the SELECT is *, will return alias_list as [None] and attribute list as [-1],
    # this * statement will be check again when pull out tuple and attribute from the csv document again.
    # The sequence is determined by the appearance in the SELECT part.
    def Selectparse(self):
        alias_list = []
        print_colume = []
        for i, tok in enumerate(self.token_list):
            if isinstance(tok, sqlparse.sql.Token) and tok.value.upper() == 'FROM':
                break
            elif str(tok.value) == "*":
                alias_list = [None]
                print_colume = [-1]
                break
            elif isinstance(tok, sqlparse.sql.IdentifierList):
                for j, k in enumerate(tok):
                    if isinstance(k, sqlparse.sql.Identifier):
                        alias_list.append(k.get_parent_name())
                        print_colume.append(k.get_real_name())
            elif isinstance(tok, sqlparse.sql.Identifier):
                alias_list.append(tok.get_parent_name())
                print_colume.append(tok.get_real_name())
            else:
                continue
        return alias_list, print_colume


    # Pair the csv name and alias name in the sequence of identifier appearance from the FROM part,
    # return csv_list (names of csv), alias_colume (a list of names of alias, alias can be None if not declared).
    def PairCsvandAlias(self):
        csv_list = []
        alias_colume = []
        index_from = -1
        index_where = len(self.token_list)
        for i, tok in enumerate(self.token_list):
            if isinstance(tok, sqlparse.sql.Token) and tok.value.upper() == 'FROM':
                index_from = i
            elif isinstance(tok, sqlparse.sql.Where):
                index_where = i
        for i, tok in enumerate(self.token_list[index_from:index_where]):
            if isinstance(tok, sqlparse.sql.IdentifierList):
                for j, k in enumerate(tok):
                    if isinstance(k, sqlparse.sql.Identifier):
                        csv_list.append(k.get_parent_name() + '.csv')
                        alias_colume.append(k.get_alias())
                        self.alias_dic[k.get_alias()] = k.get_parent_name() + '.csv'
            elif isinstance(tok, sqlparse.sql.Identifier):
                csv_list.append(tok.get_parent_name() + '.csv')
                alias_colume.append(tok.get_alias())
                self.alias_dic[tok.get_alias()] = tok.get_parent_name() + '.csv'
            else:
                continue
        return csv_list, alias_colume

    # Combine the PairCsvandAlias() and Selectparse() together. As the sequence of alias is different in each functions,
    # this function will find the corresponding list of csv names for attributes in the sequence of SELECT part.
    # If the alias is None, this function will set all csv name the same or return error
    def ProjectCsvandAlias(self):
        project_alias_name, project_attribute_name = self.Selectparse()
        pair_csv, pair_alias = self.PairCsvandAlias()
        project_csv_name = []
        for i, j in enumerate(project_alias_name):
            for k, csv_name in enumerate(pair_alias):
                if csv_name == j:
                    project_csv_name.append(pair_csv[k])
        if project_csv_name == []:
            print("error: require alias for SELECT as the final table is from multiple CSVs")
        return project_csv_name, project_alias_name, project_attribute_name


    # Parse all the conditions in the WHERE section and transfer the Bollean expression into Prefix Expression
    def Whereparse(self):
        union = []
        flag = False
        for tok in self.token_list:
            if isinstance(tok, sqlparse.sql.Where):
                condition_list = tok.tokens
                break;
        temporary_stack = []
        for i in range(len(condition_list)):
            if isinstance(condition_list[i], sqlparse.sql.Comparison):
                if flag:
                    temporary_stack.append(self.getNot(condition_list[i]))
                    flag = False
                else:
                    temporary_stack.append(condition_list[i])
            elif condition_list[i].value.upper() == 'NOT':
                flag = True
            elif condition_list[i].value.upper() == 'OR':
                union.append(temporary_stack)
                temporary_stack = []
            else:
                pass
        union.append(temporary_stack)
        return union

    # apply NOT to the conditions
    def getNOT(self, comparison):
        for tok in comparison.tokens:
            if tok.value == '=':
                tok.value = '<>'
                break
            elif tok.value == '<':
                tok.value = '>'
                break
            elif tok.value == '<=':
                tok.value = '>='
                break
            elif tok.value == '>':
                tok.value = '<'
                break
            elif tok.value == '>=':
                tok.value = '<='
                break
            elif tok.value == '<>':
                tok.value = '='
                break
            else:
                pass
        return comparison

        # Determine if there is join conditions in SQL
    def hasJoin(self):
        for tok in self.token_list:
            if isinstance(tok, sqlparse.sql.Where):
                condition_list = tok.tokens
                break;
        for i in range(len(condition_list)):
            if isinstance(condition_list[i], sqlparse.sql.Comparison):
                right_part = condition_list[i].right
                if isinstance(right_part, sqlparse.sql.Operation) or isinstance(right_part, sqlparse.sql.Identifier):
                    return True
        return False

    # Divide all the conditions into join conditions and single-table conditions
    def Classify_conditions(self, ANDconditions):
        single_index = []
        single_cond_list = []
        single_cond_dic = {}
        join_cond = []
        alias_list =[]
        for comp in ANDconditions:
            left_part = comp.left
            right_part = comp.right
            alias1, csv_path1, attrId1 = self.FindCsvpathandAttrId(left_part)
            alias_list.append(alias1)
            if isinstance(right_part, sqlparse.sql.Identifier):
                alias2, csv_path2, attrId2 = self.FindCsvpathandAttrId(right_part)
                join_cond.append(comp)
                alias_list.append(alias2)
            elif isinstance(right_part, sqlparse.sql.Operation):
                tok_list = right_part.tokens
                for ele in tok_list:
                    if isinstance(ele, sqlparse.sql.Identifier):
                        alias2, csv_path2, attrId2 = self.FindCsvpathandAttrId(ele)
                        break
                join_cond.append(comp)
                alias_list.append(alias2)
            else:
                single_cond_list.append(comp)
                single_index.append(alias1)
        table_list = list(set(alias_list))
        for t in table_list:
            single_cond_dic[t] = []
        for i in range(len(single_cond_list)):
            single_cond_dic[single_index[i]].append(single_cond_list[i])
        return table_list,single_cond_dic,join_cond

    def TransSinglecomp(self,comparison):
        left_part = comparison.left
        right_part = comparison.right
        left_btree = self.getBtree(left_part, self.indexpath)
        raw_list = []
        x= right_part.value
        if self.is_number(x):
            right_value = float(right_part.value)
        else:
            right_value = right_part.value[1:-1].upper()
        for tok in comparison.tokens:
            if tok.value == '=':
                raw_list = single_join_filter_one(left_btree, '=', right_value)
                break
            elif tok.value == '>':
                raw_list = single_join_filter_one(left_btree, '>', right_value)
                break
            elif tok.value == '<':
                raw_list = single_join_filter_one(left_btree, '<', right_value)
                break
            elif tok.value == '>=':
                raw_list = single_join_filter_one(left_btree, '>=', right_value)
                break
            elif tok.value == '<=':
                raw_list = single_join_filter_one(left_btree, '<=', right_value)
                break
            elif tok.value == '<>':
                raw_list = single_join_filter_one(left_btree, '<>', right_value)
                break
            else:
                pass
        return raw_list

    def getSingleTableQuery(self, table_list, single_cond_dic):
        result = {}
        for alias in table_list:
            C_sum =[]
            for comp in single_cond_dic[alias]:
                C = self.TransSinglecomp(comp)
                C_sum = C_sum + C
            if len(C_sum) == 0:
                output = []
            else:
                output = and_condition_single(C_sum)
            result[alias] = output
        return result


    def getJJQuery(self, JJ_cond, table_list):
        join_result =[]
        key_list = list(JJ_cond.keys())
        for i in range(len(key_list)):
            for j in range(i,len(key_list)):
                index_J1 = key_list[i]
                index_J2 = key_list[j]
                k1 = key_list[i]
                k2 = key_list[j]
                if k1 == k2:
                    for m, raw_J1 in enumerate(JJ_cond[k1]):
                        for n, raw_J2 in enumerate(JJ_cond[k2]):
                            if m < n:
                                raw_J12 = AB_AC(raw_J1, raw_J2, 0, 0)
                                raw_J1_new = raw_J12[0]
                                raw_J2_new = raw_J12[1]
                                raw_J12 = AB_AC(raw_J1_new, raw_J2_new, 1, 1)
                                JJ_cond[k1][m] = raw_J12[0]
                                JJ_cond[k2][n] = raw_J12[1]
                            else:
                                pass
                else:
                    for m, raw_J1 in enumerate(JJ_cond[k1]):
                        for n, raw_J2 in enumerate(JJ_cond[k2]):
                            if index_J1[0] == index_J2[0] and index_J1[1] != index_J2[1]:
                                raw_J12 = AB_AC(raw_J1, raw_J2, 0, 0)
                                JJ_cond[k1][m] = raw_J12[0]
                                JJ_cond[k2][n] = raw_J12[1]
                            elif index_J1[0] != index_J2[0] and index_J1[1] == index_J2[1]:
                                raw_J12 = AB_AC(raw_J1, raw_J2, 1, 1)
                                JJ_cond[k1][m] = raw_J12[0]
                                JJ_cond[k2][n] = raw_J12[1]
                            elif index_J1[0] == index_J2[1] and index_J1[1] != index_J2[0]:
                                raw_J12 = AB_AC(raw_J1, raw_J2, 0, 1)
                                JJ_cond[k1][m] = raw_J12[0]
                                JJ_cond[k2][n] = raw_J12[1]
                            elif index_J1[0] != index_J2[1] and index_J1[1] == index_J2[0]:
                                raw_J12 = AB_AC(raw_J1, raw_J2, 1, 0)
                                JJ_cond[k1][m] = raw_J12[0]
                                JJ_cond[k2][n] = raw_J12[1]
                            elif index_J1[0] == index_J2[1] and index_J1[1] == index_J2[0]:
                                raw_J12 = AB_AC(raw_J1, raw_J2, 0, 1)
                                raw_J1_new = raw_J12[0]
                                raw_J2_new = raw_J12[1]
                                raw_J12 = AB_AC(raw_J1_new, raw_J2_new, 1, 0)
                                JJ_cond[k1][m] = raw_J12[0]
                                JJ_cond[k2][n] = raw_J12[1]
                            else:
                                pass
        for k, v in JJ_cond.items():
            if len(v) > 1:
                while len(JJ_cond[k]) > 1:
                    raw_J1 = JJ_cond[k].pop()
                    raw_J2 = JJ_cond[k].pop()
                    raw_J12 = AB_AB(cross_prod(raw_J1), cross_prod(raw_J2), 0)
                    JJ_cond[k].append(raw_J12)
            elif len(v) > 0:
                raw_J1 = JJ_cond[k].pop()
                JJ_cond[k].append(cross_prod(raw_J1))
            else:
                pass
        for a in table_list:
            for b in table_list:
                if a < b and len(JJ_cond[(a, b)]) > 0 and len(JJ_cond[(b, a)]) > 0:
                    raw_J1 = JJ_cond[(a, b)].pop()
                    raw_J2 = JJ_cond[(b, a)].pop()
                    raw_J12 = AB_AB(raw_J1, raw_J2, 1)
                    JJ_cond[(a,b)].append(raw_J12)
                    del JJ_cond[(b,a)]
        for k, v in JJ_cond.items():
            if len(v) > 0:
                join_result.append([v[0],list(k)])
        return join_result


    def getFinalJoinResults(self,join_result):
        o1 = join_result.pop()
        if len(join_result) == 0:
            return [o1[0], o1[1]]
        else:
            o2 = join_result.pop()
            raw_o1 = o1[0]
            index_o1 = o1[1]
            raw_o2 = o2[0]
            index_o2 = o2[1]
            if index_o1[0] == index_o2[0] and index_o1[1] != index_o2[1]:
                raw_o12 = and_condition_double(raw_o1, raw_o2, 0, 0)
                index_o1.append(index_o2[1])
                return [raw_o12,index_o1]
            elif index_o1[0] != index_o2[0] and index_o1[1] == index_o2[1]:
                raw_o12 = and_condition_double(raw_o1, raw_o2, 1, 1)
                index_o1.append(index_o2[0])
                return [raw_o12, index_o1]
            elif index_o1[0] == index_o2[1] and index_o1[1] != index_o2[0]:
                raw_o12 = and_condition_double(raw_o1, raw_o2, 0, 1)
                index_o1.append(index_o2[0])
                return [raw_o12, index_o1]
            elif index_o1[0] != index_o2[1] and index_o1[1] == index_o2[0]:
                raw_o12 = and_condition_double(raw_o1, raw_o2, 1, 0)
                index_o1.append(index_o2[1])
                return [raw_o12, index_o1]
            else:
                return None




    def getQueryresult(self, union):
        and_sum =[]
        if self.hasJoin():
            for andC in union:
                table_list, single_cond_dic, join_cond = self.Classify_conditions(andC)
                single_result = self.getSingleTableQuery(table_list, single_cond_dic)
                JJ_cond = {}
                for a in table_list:
                    for b in table_list:
                        if a != b:
                            JJ_cond[(a,b)] =[]
                for j in join_cond:
                    raw_result = self.TransJoincomp(j, single_result)
                    JJ_cond[raw_result[1]].append(raw_result[0])
                join_result = self.getJJQuery(JJ_cond,table_list)
                final_join_result = self.getFinalJoinResults(join_result)
                if len(and_sum) == 0:
                    and_sum = final_join_result[0]
                    and_sum_ind = final_join_result[1]
                else:
                    and_sum = AB_AB_or(and_sum, final_join_result[0], 0)
            Final_result = [permute_list(and_sum), and_sum_ind]
        else:
            for andC in union:
                table_list, single_cond_dic, join_cond = self.Classify_conditions(andC)
                single_result = self.getSingleTableQuery(table_list, single_cond_dic)
                and_sum = and_sum + single_result[table_list[0]]
            Final_result = [or_condition_single(and_sum), table_list]
        return Final_result


    # Transfer Comparisons into raw query results
    def TransJoincomp(self, comparison, single_result):
        op = ''
        value = ''
        left_part = comparison.left
        right_part = comparison.right
        raw_list = []
        alias1, csv_path1, attrId1 = self.FindCsvpathandAttrId(left_part)
        if isinstance(right_part, sqlparse.sql.Operation):
            tok_list = right_part.tokens
            value = float(tok_list[-1].value)
            for ele in tok_list:
                if isinstance(ele, sqlparse.sql.Identifier):
                    alias2, csv_path2, attrId2 = self.FindCsvpathandAttrId(ele)
                elif ele.value == '+':
                    op = '+'
                    break
                elif ele.value == '-':
                    op = '-'
                    break
                elif ele.value == '*':
                    op = '*'
                    break
                elif ele.value == '/':
                    op = '/'
                    break
                else:
                    pass
        else:
            alias2, csv_path2, attrId2 = self.FindCsvpathandAttrId(right_part)
        index = (alias1, alias2)
        if single_result[alias1] == [[]] and single_result[alias2] == [[]]:
            left_btree = self.getBtree(left_part, self.indexpath)
            if isinstance(right_part, sqlparse.sql.Operation):
                right_btree = ''
                tok_list = right_part.tokens
                for ele in tok_list:
                    if isinstance(ele, sqlparse.sql.Identifier):
                        right_btree = self.getBtree(ele, self.indexpath)
                        break
                    else:
                        pass
                if op == '+':
                    for tok in comparison.tokens:
                        if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                            raw_list = double_join_filter_plus(left_btree, right_btree, tok.value, value)
                            index = (alias1, alias2)
                            break
                        elif tok.value == '>':
                            raw_list = double_join_filter_plus(right_btree, left_btree, '<', value)
                            index = (alias2, alias1)
                            break
                        elif tok.value == '>=':
                            raw_list = double_join_filter_plus(right_btree, left_btree, '<=', value)
                            index = (alias2, alias1)
                            break
                        else:
                            pass
                elif op == '-':
                    value = -1 * value
                    for tok in comparison.tokens:
                        if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                            raw_list = double_join_filter_plus(left_btree, right_btree, tok.value, value)
                            index = (alias1, alias2)
                            break
                        elif tok.value == '>':
                            raw_list = double_join_filter_plus(right_btree, left_btree, '<', value)
                            index = (alias2, alias1)
                            break
                        elif tok.value == '>=':
                            raw_list = double_join_filter_plus(right_btree, left_btree, '<=', value)
                            index = (alias2, alias1)
                            break
                        else:
                            pass
                elif op == '*':
                    for tok in comparison.tokens:
                        if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                            raw_list = double_join_filter_multi(left_btree, right_btree, tok.value, value)
                            index = (alias1, alias2)
                            break
                        elif tok.value == '>':
                            raw_list = double_join_filter_multi(right_btree, left_btree, '<', value)
                            index = (alias2, alias1)
                            break
                        elif tok.value == '>=':
                            raw_list = double_join_filter_multi(right_btree, left_btree, '<=', value)
                            index = (alias2, alias1)
                            break
                        else:
                            pass
                else:
                    value = 1 / value
                    for tok in comparison.tokens:
                        if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                            raw_list = double_join_filter_multi(left_btree, right_btree, tok.value, value)
                            index = (alias1, alias2)
                            break
                        elif tok.value == '>':
                            raw_list = double_join_filter_multi(right_btree, left_btree, '<', value)
                            index = (alias2, alias1)
                            break
                        elif tok.value == '>=':
                            raw_list = double_join_filter_multi(right_btree, left_btree, '<=', value)
                            index = (alias2, alias1)
                            break
                        else:
                            pass
            else:
                right_btree = self.getBtree(right_part, self.indexpath)
                for tok in comparison.tokens:
                    if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                        raw_list = double_join_filter(left_btree, right_btree, tok.value)
                        index = (alias1, alias2)
                        break
                    elif tok.value == '>':
                        raw_list = double_join_filter(right_btree, left_btree, '<')
                        index = (alias2, alias1)
                        break
                    elif tok.value == '>=':
                        raw_list = double_join_filter(right_btree, left_btree, '<=')
                        index = (alias2, alias1)
                        break
                    else:
                        pass
        elif single_result[alias1] == [[]]:
            left_btree = self.getBtree(left_part, self.indexpath)
            if len(single_result[alias2]) < self.opt / 2:
                if op == '':
                    with open(csv_path1, 'r', encoding="ISO-8859-1") as file1:
                        f1 = csv.reader(file1)
                        file1.seek(0)
                        file1.seek(single_result[alias1][0][0])
                        row1 = next(f1)
                        v = row1[attrId1]
                    if self.is_number(v):
                        isNumber = 1
                    else:
                        isNumber = 0
                    for tok in comparison.tokens:
                        if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                        tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                            raw_list = btree_A_a_file(left_btree, csv_path2, single_result[alias2], attrId2, tok.value, isNumber)
                            break
                        else:
                            pass
                else:
                    if op == '+':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = btree_A_a_file_plus(left_btree, csv_path2, single_result[alias2],
                                                          attrId2, tok.value, value)
                                break
                            else:
                                pass
                    elif op == '-':
                        value = -1 * value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = btree_A_a_file_plus(left_btree, csv_path2, single_result[alias2],
                                                          attrId2, tok.value, value)
                                break
                            else:
                                pass
                    elif op == '*':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = btree_A_a_file_multi(left_btree, csv_path2, single_result[alias2],
                                                          attrId2, tok.value, value)
                                break
                            else:
                                pass
                    else:
                        value = 1 / value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = btree_A_a_file_multi(left_btree, csv_path2, single_result[alias2],
                                                          attrId2, tok.value, value)
                                break
                            else:
                                pass

            else:
                with open(csv_path2, 'r', encoding="ISO-8859-1") as file2:
                    f2 = csv.reader(file2)
                    file2.seek(0)
                    file2.seek(single_result[alias2][0][0])
                    row2 = next(f2)
                    v = row2[attrId2]
                if self.is_number(v):
                    isNumber2 = 1
                else:
                    isNumber2 = 0
                right_btree = get_small_btree(csv_path2, single_result[alias2], attrId2, isNumber2)
                if op == '':
                    for tok in comparison.tokens:
                        if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                            raw_list = double_join_filter(left_btree, right_btree, tok.value)
                            break
                        elif tok.value == '>':
                            raw_list = double_join_filter(right_btree, left_btree, '<')
                            index = (alias2, alias1)
                        elif tok.value == '>=':
                            raw_list = double_join_filter(right_btree, left_btree, '<=')
                            index = (alias2, alias1)
                        else:
                            pass
                else:
                    if op == '+':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                                raw_list = double_join_filter_plus(left_btree, right_btree, tok.value, value)
                                break
                            elif tok.value == '>':
                                raw_list = double_join_filter_plus(right_btree, left_btree, '<', value)
                                index = (alias2, alias1)
                            elif tok.value == '>=':
                                raw_list = double_join_filter_plus(right_btree, left_btree, '<=',value)
                                index = (alias2, alias1)
                            else:
                                pass
                    elif op == '-':
                        value = -1 * value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                                raw_list = double_join_filter_plus(left_btree, right_btree, tok.value, value)
                                break
                            elif tok.value == '>':
                                raw_list = double_join_filter_plus(right_btree, left_btree, '<', value)
                                index = (alias2, alias1)
                            elif tok.value == '>=':
                                raw_list = double_join_filter_plus(right_btree, left_btree, '<=',value)
                                index = (alias2, alias1)
                            else:
                                pass
                    elif op == '*':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                                raw_list = double_join_filter_multi(left_btree, right_btree, tok.value, value)
                                break
                            elif tok.value == '>':
                                raw_list = double_join_filter_multi(right_btree, left_btree, '<', value)
                                index = (alias2, alias1)
                            elif tok.value == '>=':
                                raw_list = double_join_filter_multi(right_btree, left_btree, '<=',value)
                                index = (alias2, alias1)
                            else:
                                pass
                    else:
                        value = 1 / value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                                raw_list = double_join_filter_multi(left_btree, right_btree, tok.value, value)
                                break
                            elif tok.value == '>':
                                raw_list = double_join_filter_multi(right_btree, left_btree, '<', value)
                                index = (alias2, alias1)
                            elif tok.value == '>=':
                                raw_list = double_join_filter_multi(right_btree, left_btree, '<=',value)
                                index = (alias2, alias1)
                            else:
                                pass
        elif single_result[alias2] == [[]]:
            if isinstance(right_part, sqlparse.sql.Operation):
                right_btree = ''
                tok_list = right_part.tokens
                for ele in tok_list:
                    if isinstance(ele, sqlparse.sql.Identifier):
                        right_btree = self.getBtree(ele, self.indexpath)
                        break
                    else:
                        pass
            else:
                right_btree = self.getBtree(right_part, self.indexpath)
            if len(single_result[alias1]) < self.opt / 2:
                if op == '':
                    with open(csv_path2, 'r', encoding="ISO-8859-1") as file2:
                        f2 = csv.reader(file2)
                        file2.seek(0)
                        file2.seek(single_result[alias2][0][0])
                        row2 = next(f2)
                        v = row2[attrId2]
                    if self.is_number(v):
                        isNumber = 1
                    else:
                        isNumber = 0
                    for tok in comparison.tokens:
                        if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                        tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                            raw_list = A_a_btree_file(csv_path1, single_result[alias1], attrId1, right_btree, tok.value, isNumber)
                            break
                        else:
                            pass
                else:
                    if op == '+':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = A_a_btree_file_plus(csv_path1, single_result[alias1], attrId1, right_btree,
                                                               tok.value, value)
                                break
                            else:
                                pass
                    elif op == '-':
                        value = -1 * value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = A_a_btree_file_plus(csv_path1, single_result[alias1], attrId1, right_btree,
                                                               tok.value, value)
                                break
                            else:
                                pass
                    elif op == '*':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = A_a_btree_file_multi(csv_path1, single_result[alias1], attrId1, right_btree,
                                                               tok.value, value)
                                break
                            else:
                                pass
                    else:
                        value = 1 / value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = A_a_btree_file_multi(csv_path1, single_result[alias1], attrId1, right_btree,
                                                               tok.value, value)
                                break
                            else:
                                pass
            else:
                with open(csv_path1, 'r', encoding="ISO-8859-1") as file1:
                    f1 = csv.reader(file1)
                    file1.seek(0)
                    file1.seek(single_result[alias1][0][0])
                    row1 = next(f1)
                    v = row1[attrId1]
                if self.is_number(v):
                    isNumber1 = 1
                else:
                    isNumber1 = 0
                left_btree = get_small_btree(csv_path1, single_result[alias1], attrId1, isNumber1)
                if op == '':
                    for tok in comparison.tokens:
                        if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                            raw_list = double_join_filter(left_btree, right_btree, tok.value)
                            break
                        elif tok.value == '>':
                            raw_list = double_join_filter(right_btree, left_btree, '<')
                            index = (alias2, alias1)
                        elif tok.value == '>=':
                            raw_list = double_join_filter(right_btree, left_btree, '<=')
                            index = (alias2, alias1)
                        else:
                            pass
                else:
                    if op == '+':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                                raw_list = double_join_filter_plus(left_btree, right_btree, tok.value, value)
                                break
                            elif tok.value == '>':
                                raw_list = double_join_filter_plus(right_btree, left_btree, '<', value)
                                index = (alias2, alias1)
                            elif tok.value == '>=':
                                raw_list = double_join_filter_plus(right_btree, left_btree, '<=',value)
                                index = (alias2, alias1)
                            else:
                                pass
                    elif op == '-':
                        value = -1 * value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                                raw_list = double_join_filter_plus(left_btree, right_btree, tok.value, value)
                                break
                            elif tok.value == '>':
                                raw_list = double_join_filter_plus(right_btree, left_btree, '<', value)
                                index = (alias2, alias1)
                            elif tok.value == '>=':
                                raw_list = double_join_filter_plus(right_btree, left_btree, '<=',value)
                                index = (alias2, alias1)
                            else:
                                pass
                    elif op == '*':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                                raw_list = double_join_filter_multi(left_btree, right_btree, tok.value, value)
                                break
                            elif tok.value == '>':
                                raw_list = double_join_filter_multi(right_btree, left_btree, '<', value)
                                index = (alias2, alias1)
                            elif tok.value == '>=':
                                raw_list = double_join_filter_multi(right_btree, left_btree, '<=',value)
                                index = (alias2, alias1)
                            else:
                                pass
                    else:
                        value = 1 / value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                                raw_list = double_join_filter_multi(left_btree, right_btree, tok.value, value)
                                break
                            elif tok.value == '>':
                                raw_list = double_join_filter_multi(right_btree, left_btree, '<', value)
                                index = (alias2, alias1)
                            elif tok.value == '>=':
                                raw_list = double_join_filter_multi(right_btree, left_btree, '<=',value)
                                index = (alias2, alias1)
                            else:
                                pass
        else:
            if len(single_result[alias1]) + len(single_result[alias2]) < self.opt:
                with open(csv_path1, 'r', encoding="ISO-8859-1") as file1:
                    f1 = csv.reader(file1)
                    file1.seek(0)
                    file1.seek(single_result[alias1][0][0])
                    row1 = next(f1)
                    v = row1[attrId1]
                if self.is_number(v):
                    isNumber = 1
                else:
                    isNumber = 0
                if op == '':
                    for tok in comparison.tokens:
                        if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                        tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                            raw_list = A_a_B_b_file(csv_path1, single_result[alias1], attrId1, csv_path2,
                                                    single_result[alias2], attrId2, tok.value, isNumber)
                            break
                        else:
                            pass
                else:
                    if op == '+':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = A_a_B_b_file_plus(csv_path1, single_result[alias1], attrId1, csv_path2,
                                                             single_result[alias2], attrId2, tok.value)
                                break
                            else:
                                pass
                    elif op == '-':
                        value = -1 * value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = A_a_B_b_file_plus(csv_path1, single_result[alias1], attrId1, csv_path2,
                                                             single_result[alias2], attrId2, tok.value, value)
                                break
                            else:
                                pass
                    elif op == '*':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = A_a_B_b_file_multi(csv_path1, single_result[alias1], attrId1, csv_path2,
                                                              single_result[alias2], attrId2, tok.value, value)
                                break
                            else:
                                pass
                    else:
                        value = 1 / value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = A_a_B_b_file_multi(csv_path1, single_result[alias1], attrId1, csv_path2,
                                                              single_result[alias2], attrId2, tok.value, value)
                                index = (alias1, alias2)
                                break
                            else:
                                pass
            elif len(single_result[alias1]) < self.opt / 2:
                if op == '':
                    with open(csv_path2, 'r', encoding="ISO-8859-1") as file2:
                        f2 = csv.reader(file2)
                        file2.seek(0)
                        file2.seek(single_result[alias2][0][0])
                        row2 = next(f2)
                        v = row2[attrId2]
                    if self.is_number(v):
                        isNumber = 1
                    else:
                        isNumber = 0
                    right_btree = get_small_btree(csv_path2, single_result[alias2], attrId2, isNumber)
                    for tok in comparison.tokens:
                        if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                        tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                            raw_list = A_a_btree_file(csv_path1, single_result[alias1], attrId1, right_btree, tok.value, isNumber)
                            break
                        else:
                            pass
                else:
                    right_btree = get_small_btree(csv_path2, single_result[alias2], attrId2, 1)
                    if op == '+':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = A_a_btree_file_plus(csv_path1, single_result[alias1], attrId1, right_btree,
                                                               tok.value, value)
                                break
                            else:
                                pass
                    elif op == '-':
                        value = -1 * value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = A_a_btree_file_plus(csv_path1, single_result[alias1], attrId1, right_btree,
                                                               tok.value, value)
                                break
                            else:
                                pass
                    elif op == '*':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = A_a_btree_file_multi(csv_path1, single_result[alias1], attrId1, right_btree,
                                                               tok.value, value)
                                break
                            else:
                                pass
                    else:
                        value = 1 / value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = A_a_btree_file_multi(csv_path1, single_result[alias1], attrId1, right_btree,
                                                               tok.value, value)
                                break
                            else:
                                pass
            elif len(single_result[alias2]) < self.opt / 2:
                if op == '':
                    with open(csv_path1, 'r', encoding="ISO-8859-1") as file1:
                        f1 = csv.reader(file1)
                        file1.seek(0)
                        file1.seek(single_result[alias1][0][0])
                        row1 = next(f1)
                        v = row1[attrId1]
                    if self.is_number(v):
                        isNumber = 1
                    else:
                        isNumber = 0
                    left_btree = get_small_btree(csv_path1, single_result[alias1], attrId1, isNumber)
                    for tok in comparison.tokens:
                        if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                        tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                            raw_list = btree_A_a_file(left_btree, csv_path2, single_result[alias2], attrId2, tok.value, isNumber)
                            break
                        else:
                            pass
                else:
                    left_btree = get_small_btree(csv_path1, single_result[alias1], attrId1, 1)
                    if op == '+':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = btree_A_a_file_plus(left_btree, csv_path2, single_result[alias2],
                                                          attrId2, tok.value, value)
                                break
                            else:
                                pass
                    elif op == '-':
                        value = -1 * value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = btree_A_a_file_plus(left_btree, csv_path2, single_result[alias2],
                                                          attrId2, tok.value, value)
                                break
                            else:
                                pass
                    elif op == '*':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = btree_A_a_file_multi(left_btree, csv_path2, single_result[alias2],
                                                          attrId2, tok.value, value)
                                break
                            else:
                                pass
                    else:
                        value = 1 / value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '>' or \
                                            tok.value == '<=' or tok.value == '>=' or tok.value == '<>':
                                raw_list = btree_A_a_file_multi(left_btree, csv_path2, single_result[alias2],
                                                          attrId2, tok.value, value)
                                break
                            else:
                                pass
            else:
                with open(csv_path1, 'r', encoding="ISO-8859-1") as file1:
                    f1 = csv.reader(file1)
                    file1.seek(0)
                    file1.seek(single_result[alias1][0][0])
                    row1 = next(f1)
                    v = row1[attrId1]
                if self.is_number(v):
                    isNumber1 = 1
                else:
                    isNumber1 = 0
                left_btree = get_small_btree(csv_path1, single_result[alias1], attrId1, isNumber1)
                with open(csv_path2, 'r', encoding="ISO-8859-1") as file2:
                    f2 = csv.reader(file2)
                    file2.seek(0)
                    file2.seek(single_result[alias2][0][0])
                    row2 = next(f2)
                    v = row2[attrId2]
                if self.is_number(v):
                    isNumber2 = 1
                else:
                    isNumber2 = 0
                right_btree = get_small_btree(csv_path2, single_result[alias2], attrId2, isNumber2)
                if op == '':
                    for tok in comparison.tokens:
                        if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                            raw_list = double_join_filter(left_btree, right_btree, tok.value)
                            break
                        elif tok.value == '>':
                            raw_list = double_join_filter(right_btree, left_btree, '<')
                            index = (alias2, alias1)
                        elif tok.value == '>=':
                            raw_list = double_join_filter(right_btree, left_btree, '<=')
                            index = (alias2, alias1)
                        else:
                            pass
                else:
                    if op == '+':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                                raw_list = double_join_filter_plus(left_btree, right_btree, tok.value, value)
                                break
                            elif tok.value == '>':
                                raw_list = double_join_filter_plus(right_btree, left_btree, '<', value)
                                index = (alias2, alias1)
                            elif tok.value == '>=':
                                raw_list = double_join_filter_plus(right_btree, left_btree, '<=',value)
                                index = (alias2, alias1)
                            else:
                                pass
                    elif op == '-':
                        value = -1 * value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                                raw_list = double_join_filter_plus(left_btree, right_btree, tok.value, value)
                                break
                            elif tok.value == '>':
                                raw_list = double_join_filter_plus(right_btree, left_btree, '<', value)
                                index = (alias2, alias1)
                            elif tok.value == '>=':
                                raw_list = double_join_filter_plus(right_btree, left_btree, '<=',value)
                                index = (alias2, alias1)
                            else:
                                pass
                    elif op == '*':
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                                raw_list = double_join_filter_multi(left_btree, right_btree, tok.value, value)
                                break
                            elif tok.value == '>':
                                raw_list = double_join_filter_multi(right_btree, left_btree, '<', value)
                                index = (alias2, alias1)
                            elif tok.value == '>=':
                                raw_list = double_join_filter_multi(right_btree, left_btree, '<=',value)
                                index = (alias2, alias1)
                            else:
                                pass
                    else:
                        value = 1 / value
                        for tok in comparison.tokens:
                            if tok.value == '=' or tok.value == '<' or tok.value == '<=' or tok.value == '<>':
                                raw_list = double_join_filter_multi(left_btree, right_btree, tok.value, value)
                                break
                            elif tok.value == '>':
                                raw_list = double_join_filter_multi(right_btree, left_btree, '<', value)
                                index = (alias2, alias1)
                            elif tok.value == '>=':
                                raw_list = double_join_filter_multi(right_btree, left_btree, '<=',value)
                                index = (alias2, alias1)
                            else:
                                pass
        raw_result = [raw_list, index]
        return raw_result


    # Find csv name for the corresponding attribute
    def FindCsvpathandAttrId(self, tok):
        alias = tok.get_parent_name()
        csv_path = self.alias_dic[alias]
        attribute = tok.get_real_name()
        attrId = getAttrID(csv_path, attribute)
        return alias, csv_path, attrId


    # get Btree file path for the corresponding attribute
    def getBtree(self, tok, indexpath):
        alias,csv_path, attrId = self.FindCsvpathandAttrId(tok)
        csv_name = ntpath.basename(csv_path)
        btree_path = indexpath + csv_name.split('.')[0] + '_Attr_' + str(attrId) + '_.tree'
        return btree_path


    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False