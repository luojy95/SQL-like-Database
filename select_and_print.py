import sqlparse
import csv
import time
from prettytable import PrettyTable


def Main():

	sql_statement = "SELECT M.title_year, M.movie_title, A.Award, M.imdb_score, M.movie_facebook_likes FROM movies.csv M JOIN oscars.csv A ON (M.movie_title = A.Film) WHERE A.Winner = 1 AND (M.imdb_score < 6 OR M.movie_facebook_likes < 10000)"

	alias_index_result = ['A', 'M']
	rowindice_result_from_selection = [[3928,3928,1894,783], [18,22,30,32]]
	ProjectAndPrint(sql_statement, rowindice_result_from_selection, alias_index_result)



# The packaged function which take the input of sql_statement and a 2-order list of indice in the appearance sequence of csv name in FROM part, it will print the result indicated by the SELECT part.
def ProjectAndPrint(sql_statement, rowindice_result_from_selection, alias_index_result):
	#sql_statement: the statement of sql query
	#rowindice_result_from_selection: the 2-level list of row indice with sequence corresponding to the alias_index_result
	#alas_index_result: the list of alias, should be the same sequence corresponding to the rowindice_result_from_selection
	print("start the final projection and printing")
	matched_rowindice_lists = MatchIndicewithAliasAttribute(sql_statement, rowindice_result_from_selection, alias_index_result)
	pro_csv_names, pro_alias_names, pro_attribute_names = ProjectCsvandAlias(sql_statement)
	fin_attributes, fin_result = FindValueinMultipleCsv(pro_csv_names, matched_rowindice_lists, pro_attribute_names)
	print("---------------------the result of query is as followed:-----------------------")
	pr = PrettyTable(fin_attributes)
	for i, row in enumerate(fin_result):
		pr.add_row(row)
	print(pr)


# the function to print the final table line by line, list_name is the statement representing the final table
def printlist(list_name):
	for i, row in enumerate(list_name):
		print(row)


# the function the parse the SELECT part (before FROM) with sql statement as the input. If the SELECT is not *, the outpub is a list of alias (can be None is no alias provided) and a list of the corresponding attribute. If the SELECT is *, will return alias_list as [None] and attribute list as [-1], this * statement will be check again when pull out tuple and attribute from the csv document again. The sequence is determined by the appearance in the SELECT part.
def Selectparse(sql):
	# print("start parse selection part")
	alias_list = []
	attribute_list = []
	print_colume = []
	parsed = sqlparse.parse(sql)
	result = parsed[0]
	token_list = result.tokens
	for i, tok in enumerate(token_list):
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

# Pair the csv name and alias name in the sequence of identifier appearance from the FROM part, return csv_list (names of csv), alias_colume (a list of names of alias, alias can be None if not declared).
def PairCsvandAlias(sql):
	# print("start find alias for csv")
	csv_list = []
	alias_list = []
	alias_colume = []
	parsed = sqlparse.parse(sql)
	result = parsed[0]
	token_list = result.tokens
	index_from = -1
	index_where = len(token_list)
	for i, tok in enumerate(token_list):
		if isinstance(tok, sqlparse.sql.Token) and tok.value.upper() == 'FROM':
			index_from = i
		elif isinstance(tok, sqlparse.sql.Token) and tok.value.upper() == 'WHERE':
			index_where = i		
	for i, tok in enumerate(token_list[index_from:index_where]):
		if isinstance(tok, sqlparse.sql.IdentifierList):
			for j, k in enumerate(tok):
				if isinstance(k, sqlparse.sql.Identifier):
					csv_list.append(k.get_parent_name()+'.csv')
					alias_colume.append(k.get_alias())
		elif isinstance(tok, sqlparse.sql.Identifier):
				csv_list.append(tok.get_parent_name()+'.csv')
				alias_colume.append(tok.get_alias())
		else:
			continue
	return csv_list, alias_colume


# Combine the PairCsvandAlias() and Selectparse() together. As the sequence of alias is different in each functions, this function will find the corresponding list of csv names for attributes in the sequence of SELECT part. If the alias is None, this function will set all csv name the same or return error
def ProjectCsvandAlias(sql):
	project_alias_name, project_attribute_name = Selectparse(sql)
	pair_csv, pair_alias = PairCsvandAlias(sql)
	project_csv_name = []
	for i, j in enumerate(project_alias_name):
		for k, csv_name in enumerate(pair_alias):
			if csv_name == j:
				project_csv_name.append(pair_csv[k])
	if project_csv_name == []:
		print("error: require alias for SELECT as the final table is from multiple CSVs")
	return project_csv_name, project_alias_name, project_attribute_name

def Findcsvname(alias):
	pair_csv, pair_alias = PairCsvandAlias(sql)
	for i, j in enumerate(pair_alias):
		if j == alias:
			return pair_csv[i]

def FindCsvnameandAttribute(tok):
	csv_name = ''
	alias = ''
	attribute = ''
	if isinstance(tok, sqlparse.sql.Identifier):
		alias = tok.get_parent_name()
		attribute = tok.get_real_name()
	csv_name = Findcsvname(alias)
	return csv_name, attribute


# As the list of indice is in the sequence of appearance in the FROM part, this function will match the indice list according the attribute and csv in the SELECT part
def MatchIndicewithAliasAttribute(sql, rowindice_result_from_selection, alias_index_from_result):
	p_csv_names, p_alias_names, p_attribute_names = ProjectCsvandAlias(sql)
	f_csv_names, f_alias_names = PairCsvandAlias(sql)
	matched_rowindice_lists = []
	if len(f_csv_names) != len(rowindice_result_from_selection):
		print("no selection result matched the conditions or error: the row indice list after selection is incorrect")
	else:
		for i, csaname in enumerate(p_alias_names):
			i_in_f = alias_index_from_result.index(csaname)
			matched_rowindice_lists.append(rowindice_result_from_selection[i_in_f])
	if matched_rowindice_lists == []:
		print("no selection result matched the conditions or error with indice")
	return matched_rowindice_lists

# just to check if all element in a list is the same
def all_same(items):
    return all(x == items[0] for x in items)

# This function take one open csv file, a list of row_indice for one csv, a list of attribute (in the SELECT part) as input and return the attribute name and value result in the tuple form. Note that this function service the FindValueinMultipleCsv() function as this function only accepted single filename and single row_indice list for one csv.
def Findvalueincsv(filename, row_indice, volume_value_list):
	name = filename
	with open(name, 'r', encoding="utf8") as filename_open:
		f = csv.reader(filename_open)
		filename_open.seek(0)
		row1 = next(f)
		volume_index = []
		value_result = [('Null',)]*len(row_indice)
		attribute_tuple = []
		attribute_name_list = []

		# the list of attribute name corresponding to the final attribute_tuple, in case some volume in volume_value_list has values that are not an attribute in f

		if volume_value_list == [-1]: # corresponding to the Selectparse(sql) function, if SELECT *, should print all
			volume_value_list = list(row1)
		for i, value in enumerate(volume_value_list):
			for m in range(0, len(row1)):
				if row1[m] == value:
					volume_index.append(m)
					attribute_name_list.append(value)
		for k, row in enumerate(f):
			for j, ind in enumerate(row_indice):
				if ind == k+1:
					for j, h in enumerate(volume_index):
						if row[h] != '':
							attribute_tuple.append(row[h])
						else:
							attribute_tuple.append('')
					indice_samevalue = indices(row_indice, k+1)
					for insame in indice_samevalue:
						value_result[insame] = tuple(attribute_tuple)
					attribute_tuple = []
			if k == row_indice[len(row_indice)-1]:
				break

		if volume_index == [] or value_result == []:
			print("error: cannot find attribute in csv with referenced name or with the row indice")
		#print(volume_value_list)	
		attribute_name_tuple = tuple(attribute_name_list)
	return attribute_name_tuple, value_result


def indices(mylist, value):
    return [i for i,x in enumerate(mylist) if x==value]




# This function take a list of open csv file, a 2-level list of row_indice for multiple csv, a list of attribute (in the SELECT part) as input and return the attribute name and value result in the tuple form. 
def FindValueinMultipleCsv(csv_list, tuplelist_for_csvs, attribute_list):
	result_list = []
	final_result = []
	attributelist_for_csvs = []
	final_attributelist = []
	separate_attribute=[]
	separate_result = []
	for i, file in enumerate(csv_list):
		separate_attribute, separate_result = Findvalueincsv(file, tuplelist_for_csvs[i], [attribute_list[i]])
		final_attributelist += separate_attribute
		if final_result == []:
			final_result = separate_result
		else:
			final_result = [final_result[n] + separate_result[n] for n in range(len(separate_result))]
	return final_attributelist, final_result


if __name__ == '__main__':
	Main()




