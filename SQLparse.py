import sqlparse
from myCSV import *
import ntpath
from join import *

class Sql_parsing(object):

    def __init__(self, sql, indexpath):
        # Currently supports only standard SELECT statements
        # Holds original SQL
        self.sql = sql
        self.parsed = sqlparse.parse(sql)
        self.token_list = self.parsed[0].tokens
        self.alias_dic = {}
        self.indexpath = indexpath

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

    # Define the operation of dealing with AND operator when generating Prefix Expression
    def ANDop(self, ele, temporary_stack, prefix):
        if len(temporary_stack) == 0:
            temporary_stack.append(ele)
            return temporary_stack, prefix
        if temporary_stack[-1].value.upper() == 'NOT':
            a = temporary_stack.pop()
            prefix.append(a)
            temporary_stack, prefix = self.ANDop(ele, temporary_stack, prefix)
            return temporary_stack, prefix
        else:
            temporary_stack.append(ele)
            return temporary_stack, prefix

    def ORop(self, ele, temporary_stack, prefix):
        if len(temporary_stack) == 0 or temporary_stack[-1].value.upper() == 'OR':
            temporary_stack.append(ele)
            return temporary_stack, prefix
        else:
            a = temporary_stack.pop()
            prefix.append(a)
            temporary_stack, prefix = self.ORop(ele, temporary_stack, prefix)
            return temporary_stack, prefix


    # Parse all the conditions in the WHERE section and transfer the Bollean expression into Prefix Expression
    def Whereparse(self):
        prefix = []
        for tok in self.token_list:
            if isinstance(tok, sqlparse.sql.Where):
                condition_list = tok.tokens
                break;
        temporary_stack = []
        for i in range(len(condition_list)):
            ele = condition_list.pop()
            if isinstance(ele, sqlparse.sql.Comparison):
                prefix.append(ele)
            elif ele.value.upper() == 'NOT' or len(temporary_stack) == 0:
                temporary_stack.append(ele)
            elif ele.value.upper() == 'AND':
                temporary_stack,prefix= self.ANDop(ele,temporary_stack,prefix)
            elif ele.value.upper() == 'OR':
                temporary_stack, prefix = self.ORop(ele, temporary_stack, prefix)
        for j in range(len(temporary_stack)):
            op = temporary_stack.pop()
            prefix.append(op)
        return prefix

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
        btree_path = indexpath + '/' + csv_name.split('.')[0] + '_Attr_' + str(attrId) + '_.tree'
        return btree_path

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    # Transfer Comparisons into readable form
    def Transcomp(self, comparison):
        left_part = comparison.left
        right_part = comparison.right
        left_btree = self.getBtree(left_part,self.indexpath)
        index = []
        if self.is_number(right_part.value):
            alias, csv_path, attrId = self.FindCsvpathandAttrId(left_part)
            index.append()
            right_number = float(right_part.value)
            for tok in comparison.tokens:
                if tok.value == '=':
                    result = single_join_filter_one(left_btree, '=', right_number)
                elif tok.value == '>':
                    result = single_join_filter_one(left_btree, '>', right_number)
                elif tok.value == '<':
                    result = single_join_filter_one(left_btree, '<', right_number)
                elif tok.value == '>=':
                    result = single_join_filter_one(left_btree, '>=', right_number)
                elif tok.value == '<=':
                    result = single_join_filter_one(left_btree, '<=', right_number)
                else:
                    result = single_join_filter_one(left_btree, '<>', right_number)
        elif isinstance(right_part, sqlparse.sql.Identifier):
            right_btree = self.getBtree(right_part,self.indexpath)
            for tok in comparison.tokens:
                if tok.value == '=':
                    pass
                elif tok.value == '>':
                    pass
                elif tok.value == '<':
                    pass
                elif tok.value == '>=':
                    pass
                elif tok.value == '<=':
                    pass
                else:
                    pass
        else:



