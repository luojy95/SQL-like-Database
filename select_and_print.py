import sqlparse
import csv
import time
import pandas as pd
#sql_statement = 'select xman.attr from foo'
# sql_statement = "SELECT M.movie_facebook_likes FROM movies.csv M JOIN oscars.csv A ON M.movie_title = A.Film JOIN business.csv B ON M.rating = B.stars AND M.sales < B.networth WHERE A.Winner = 1 AND (M.imdb_score < 6 OR M.movie_facebook_likes < 10000) AND M.title LIKE 'Face'"
# parsed = sqlparse.parse(sql_statement)
# result = parsed[0]
# #print(result)
# #print(result.tokens[2].ttype)
# print(isinstance(result.tokens[2], sqlparse.sql.Identifier))
# testtoken = sqlparse.sql.Token
#print(isinstance(parsed[0], sqlparse.sql.TokenList))
#print(testtoken.is_whitespace)


def Main():
	# sql_statement = "SELECT M.movie_facebook_likes, A.Film, M.Title  FROM movies.csv M JOIN oscars.csv A ON M.movie_title = A.Film JOIN business.csv B ON M.rating = B.stars AND M.sales < B.networth WHERE A.Winner = 1 AND (M.imdb_score < 6 OR M.movie_facebook_likes < 10000) AND M.title LIKE 'Face'"
	sql_statement = "SELECT M.movie_title, M.director_name, A.date, A.useful, A.cool FROM movies.csv M, review_500k.csv A"
	#sql_statement = "SELECT * FROM movies.csv"
	rowindice_result_from_selection = [[1000,1000,1000,1000], [2000,3000,4000,10000]]
	start = time.time()
	ProjectAndPrint(sql_statement, rowindice_result_from_selection)
	time_elapse = time.time()-start
	print(time_elapse)
	#sql_statement = "SELECT facebook, google, amazon FROM movie.csv M"
	#result1 = Selectparse(sql_statement)
	#print(result1)
	# print("------------------------")
	#result2 = PairCsvandAlias(sql_statement)
	#print(result2)
	# print("-------------------------------")
	# result3 = ProjectCsvandAlias(sql_statement)
	# print(result3)

	# print("start prepare step 1")
	# start = time.time()
	# print("start the final projection and printing")
	# matched_rowindice_lists = MatchIndicewithAliasAttribute(sql_statement, rowindice_result_from_selection)
	# #opencsv_files, rowindice_lists = PrepareCsvopenfileAndIndiceMatch(sql_statement, rowindice_result_from_selection)
	# # print(opencsv_files, rowindice_lists)
	# # print("start prepare step 2----")
	# pro_csv_names, pro_alias_names, pro_attribute_names = ProjectCsvandAlias(sql_statement)
	# fin_attributes, fin_result = FindValueinMultipleCsv(pro_csv_names, matched_rowindice_lists, pro_attribute_names)
	# print("--------the result of query is as followed:------------")
	# print(fin_attributes)
	# printlist(fin_result)
	# time_elapse = time.time()-start
	# print(time_elapse)
	# print("pro_csv_names, pro_alias_names, pro_attribute_names are:")
	# print(pro_csv_names, pro_alias_names, pro_attribute_names)
	# print("start prepare step 3---------")

	# print(opencsv_files, rowindice_lists, pro_attribute_names)
	# fin_attributes, fin_result = FindValueinMultipleCsv(opencsv_files, rowindice_lists, pro_attribute_names)
	# print("--------------debug opencsv_files")
	# name1 = 'movies.csv'
	# name2 = 'review_500k.csv'
	# with open(name1, 'r', encoding="utf8") as filename1:
	# 	with open(name2, 'r', encoding="utf8") as filename2:
	# 		start = time.time()
	# 		opencsv_files = [filename1, filename1, filename2, filename2, filename2]
	# 		#print(opencsv_files, rowindice_lists, pro_attribute_names)
	# 		fin_attributes, fin_result = FindValueinMultipleCsv(opencsv_files, rowindice_lists, pro_attribute_names)
	# 		print("--------the result of query is as followed:------------")
	# 		print(fin_attributes)
	# 		printlist(fin_result)
	# 		time_elapse = time.time()-start
	# 		print(time_elapse)

# The packaged function which take the input of sql_statement and a 2-order list of indice in the appearance sequence of csv name in FROM part, it will print the result indicated by the SELECT part
def ProjectAndPrint(sql_statement, rowindice_result_from_selection):
	#start = time.time()
	print("start the final projection and printing")
	matched_rowindice_lists = MatchIndicewithAliasAttribute(sql_statement, rowindice_result_from_selection)
	#opencsv_files, rowindice_lists = PrepareCsvopenfileAndIndiceMatch(sql_statement, rowindice_result_from_selection)
	# print(opencsv_files, rowindice_lists)
	# print("start prepare step 2----")
	pro_csv_names, pro_alias_names, pro_attribute_names = ProjectCsvandAlias(sql_statement)
	fin_attributes, fin_result = FindValueinMultipleCsv(pro_csv_names, matched_rowindice_lists, pro_attribute_names)
	print("--------the result of query is as followed:------------")
	print(fin_attributes)
	printlist(fin_result)
	#time_elapse = time.time()-start
	#print(time_elapse)

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
		#print(isinstance(tok, sqlparse.sql.Token))
		#print(tok.ttype, str(tok.value))
#		if tok.ttype == 'Token.Keyword' and str(tok.value).upper() == "FROM":
		if isinstance(tok, sqlparse.sql.Token) and tok.value.upper() == 'FROM':
			break
		#elif tok.ttype == 'Token.Wildcard' and str(tok.value) == "*":
		elif str(tok.value) == "*":
			# alias_list = ['None']
			alias_list = [None]
			print_colume = [-1]
			break
		elif isinstance(tok, sqlparse.sql.IdentifierList):
			for j, k in enumerate(tok):
	#			iden = tok.get_identifiers()
				if isinstance(k, sqlparse.sql.Identifier):
					alias_list.append(k.get_parent_name())
					print_colume.append(k.get_real_name())
			#alias.append(iden.get_alias())
	#		attributelist.append(tok.)
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
		#print(isinstance(tok, sqlparse.sql.Token))
		#print(tok.ttype, str(tok.value))
#		if tok.ttype == 'Token.Keyword' and str(tok.value).upper() == "FROM":
		if isinstance(tok, sqlparse.sql.IdentifierList):
			for j, k in enumerate(tok):
	#			iden = tok.get_identifiers()
				if isinstance(k, sqlparse.sql.Identifier):
					csv_list.append(k.get_parent_name()+'.csv')
					alias_colume.append(k.get_alias())
			#alias.append(iden.get_alias())
	#		attributelist.append(tok.)
		elif isinstance(tok, sqlparse.sql.Identifier):
				csv_list.append(tok.get_parent_name()+'.csv')
				alias_colume.append(tok.get_alias())
		else:
			continue
	return csv_list, alias_colume
#def ProjectionPrint

# Combine the PairCsvandAlias() and Selectparse() together. As the sequence of alias is different in each functions, this function will find the corresponding list of csv names for attributes in the sequence of SELECT part. If the alias is None, this function will set all csv name the same or return error
def ProjectCsvandAlias(sql):
	# print("get the csv_name and attribute_name for projection")
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
		attribute = get_real_name()
	csv_name = Findcsvname(alias)
	return csv_name, attribute


# As the list of indice is in the sequence of appearance in the FROM part, this function will match the indice list according the attribute and csv in the SELECT part
def MatchIndicewithAliasAttribute(sql, rowindice_result_from_selection):
	p_csv_names, p_alias_names, p_attribute_names = ProjectCsvandAlias(sql)
	f_csv_names, f_alias_names = PairCsvandAlias(sql)
	matched_rowindice_lists = []
	# print(len(f_csv_names))
	# print(len(rowindice_result_from_selection))
	if len(f_csv_names) != len(rowindice_result_from_selection):
		print("no selection result matched the conditions or error: the row indice list after selection is incorrect")
	else:
		for i, csaname in enumerate(p_csv_names):
			i_in_f = f_csv_names.index(csaname)
			matched_rowindice_lists.append(rowindice_result_from_selection[i_in_f])
	if matched_rowindice_lists == []:
		print("no selection result matched the conditions or error with indice")
	return matched_rowindice_lists

# Service the Findvalueincsv(), parse the sql statement to find the csv list in the appearance sequence in FROM and open them to construct a list. May be malfunction when combining with PrepareCsvopenfileAndIndiceMatch()
# def CsvReaderWithSql(sql):
# 	f_csv_names, f_alias_names = PairCsvandAlias(sql)
# 	file_opencsv = []
# 	for i, csvname in enumerate(f_csv_names):
# 		with open(csvname, 'r', encoding="utf8") as filename:
# 			file_opencsv.append(filename)
# 	return file_opencsv

# As the list of the openfile is in the sequence of appearance in the FROM part, this function will match the open file list according the attribute and csv in the SELECT part, May be malfunction when combining with PrepareCsvopenfileAndIndiceMatch()
# def MatchFileswithAliasAttribute(sql, file_open_list):
# 	p_csv_names, p_alias_names, p_attribute_names = ProjectCsvandAlias(sql)
# 	f_csv_names, f_alias_names = PairCsvandAlias(sql)
# 	matched_file_open_lists = []
# 	if len(f_csv_names) != len(file_open_list):
# 		print("error: no file is opened in file open list")
# 	else:
# 		for i, csaname in enumerate(p_csv_names):
# 			i_in_f = f_csv_names.index(csaname)
# 			matched_file_open_lists.append(file_open_list[i_in_f])
# 	if matched_file_open_lists == []:
# 		print("error: open csv file match alias.attribute failed")
# 	return matched_file_open_lists

# integrate the match file with alias attribute and match indice with alias attribute into one function
# def PrepareCsvopenfileAndIndiceMatch(sql, rowindice_result_from_selection):
# 	opencsv_file = CsvReaderWithSql(sql)
# 	# print(opencsv_file)
# 	matched_opencsv_file = MatchFileswithAliasAttribute(sql, opencsv_file)
# 	# print(matched_opencsv_file)
# 	matched_rowindice_lists = MatchIndicewithAliasAttribute(sql, rowindice_result_from_selection)
# 	# print(matched_rowindice_lists)
# 	return matched_opencsv_file, matched_rowindice_lists


# just to check if all element in a list is the same
def all_same(items):
    return all(x == items[0] for x in items)

# def Findvalueincsv_1(f, row_list, volume_list):
# 	#return (row[volume]) for row in row_list
# 	return (filter(lambda a: a != '', row[volume_list]) \
#     for row in row_list)

# This function take one open csv file, a list of row_indice for one csv, a list of attribute (in the SELECT part) as input and return the attribute name and value result in the tuple form. Note that this function service the FindValueinMultipleCsv() function as this function only accepted single filename and single row_indice list for one csv.
def Findvalueincsv(filename, row_indice, volume_value_list):
	#print(filename)
	#name = 'review-500k.csv'
	name = filename
	with open(name, 'r', encoding="utf8") as filename_open:
		f = csv.reader(filename_open)
		filename_open.seek(0)
		row1 = next(f)
		volume_index = []
		# print("the row1 is:"+row1[0])
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
			# if i == len(volume_value_list)-1:
		# print(volume_index)	# 	break
		for k, row in enumerate(f):
	#		for n, ri in enumerate(row_indice):
	#			if k+2 == ri:
			for j, ind in enumerate(row_indice):
				if ind == k+2:
					#print("k is:",k,"row is:",ind)
				#if row_indice in row_indice:
					for j, h in enumerate(volume_index):
						#print(j)
						#print(k+2, row[h])
						if row[h] != '':
							attribute_tuple.append(row[h])
						else:
							attribute_tuple.append('')
					#value_result.append(attribute_tuple)
					#value_result.append(tuple(attribute_tuple))
					indice_samevalue = indices(row_indice, k+2)
					#print("indice_same value is:",indice_samevalue)
					#row_indice.index(k+2)
					#print(row_indice.index(k+2))
					for insame in indice_samevalue:
					# value_result[row_indice.index(k+2)] = tuple(attribute_tuple)
						value_result[insame] = tuple(attribute_tuple)
					#print(row_indice.index(k+2), k+2)
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


# may need to find the corresponding tuplelist in another function. Currently assume the tuple list_for-csvs the same sequence as the distinct_csv_list. Here the csv_list is not the name but the list of opened result = csv.reader(filename) for time saving purpose
# in this result, the final sequence is in the sequence of distinct_csv_list and corresponding attribute_list

# def FindValueinMultipleCsv(csv_list, tuplelist_for_csvs, attribute_list)
# 	result_list = []
# 	final_result = []
# 	distinct_csv_list = list(set(csv_list))
# 	attributelist_for_csvs = []
# 	final_attributelist = []
# 	separate_attribute=[]
# 	separate_result = []
# 	for i, file in enumerate(distinct_csv_list):
# 		separate_attribute, separate_result = Findvalueincsv(file, tuplelist_for_csvs[:,i], attribute_list)
# 		result_list.append(separate_result)
# 		attributelist_for_csvs.append(separate_attribute)
# 		separate_attribute=[]
# 		separate_result = []
# 	if len(csv_list) == 1:
# 		final_result = result_list
# 		final_attributelist = attributelist_for_csvs[0]
# 	if len(csv_list) == 2:
# 		final_result = [[result_list[0][i], result_list[1][i]] for i in range(len(result_list[0]))]
# 		final_attributelist = [attributelist_for_csvs[0], attributelist_for_csvs[1]]
# 	if len(csv_list) == 3:
# 		final_result = [[result_list[0][i], result_list[1][i], result_list[2][i]] for i in range(len(result_list[0]))]
# 		final_attributelist = [attributelist_for_csvs[0], attributelist_for_csvs[1], attributelist_for_csvs[2]]
# 	return final_attributelist, final_result

# csv_list should be an object of "open(name, 'r', encoding="utf8")" but not csv.reader

# This function take a list of open csv file, a 2-level list of row_indice for multiple csv, a list of attribute (in the SELECT part) as input and return the attribute name and value result in the tuple form. 
def FindValueinMultipleCsv(csv_list, tuplelist_for_csvs, attribute_list):
	# print("############")
	# print(csv_list, tuplelist_for_csvs, attribute_list)
	# print("$$$$")
	result_list = []
	final_result = []
	#istinct_csv_list = set(csv_list)
	attributelist_for_csvs = []
	final_attributelist = []
	separate_attribute=[]
	separate_result = []
	# for i, file in enumerate(distinct_csv_list):
	# 	separate_attribute, separate_result = Findvalueincsv(file, tuplelist_for_csvs[:,i], attribute_list)
	# 	result_list.append(separate_result)
	# 	attributelist_for_csvs.append(separate_attribute)
	# 	separate_attribute=[]
	# 	separate_result = []
	# if all_same(csv_list):
	# 	final_attributelist, final_result = Findvalueincsv(csv_list[0], tuplelist_for_csvs[0], attribute_list)
	# if all_same(csv_list) == False:
	for i, file in enumerate(csv_list):
		# print(csv_list[i], tuplelist_for_csvs[i], attribute_list[i])
		separate_attribute, separate_result = Findvalueincsv(file, tuplelist_for_csvs[i], [attribute_list[i]])
		# print(separate_attribute)
		# print(separate_result)
		# print("within the function--------------")
		final_attributelist += separate_attribute
		#final_result += separate_result
		# print(separate_result)
		if final_result == []:
			final_result = separate_result
		else:
			final_result = [final_result[n] + separate_result[n] for n in range(len(separate_result))]
	# if len(csv_list) == 3:
	# 	final_result = [[result_list[0][i], result_list[1][i], result_list[2][i]] for i in range(len(result_list[0]))]
	# 	final_attributelist = [attributelist_for_csvs[0], attributelist_for_csvs[1], attributelist_for_csvs[2]]
	return final_attributelist, final_result




# def MergeCsvandAttributeList(csv_list, attribute_list):
# 	new_csv_attribute_







#find the corresponding value in csv (class:csv.reader) in row row_list and volume volume
# def Findvalueincsv(f, row, volume)
# 	return (row[volume]) for row in row_list


# def PrintResult(tuple_indice_list, sql)
# 	project_csv_name, project_alias_name, project_attribute_name = ProjectCsvandAlias(sql)
# 	csv_reader = []
# 	for i, k in enumerate(project_csv_name)
# 		with open ('', project_csv_name, 'rb') as filename:
# 			csv_reader.append(csv.reader(filename))
# 			#start = time.time()

# 			for i, row in enumerate(reader):
# 				print(i)
# 				if i in range(300,500):
# 					print(row[0])
# 				else:
# 					pass


if __name__ == '__main__':
	Main()




