# DB_jzlx_plus

This directory contains code of our database system, which is designed to handle sql-like queries, 
i.e., SELECT-FROM-WHERE.

--------------------------------------------------------------------------------------------------------------------

SQLparse.py: parse SQL input, optimize query and output query result.

Terminal.py: include user interface that allow users to Preprocess, Build index, run query, etc.

index_management.py: build dictionary for btree

join.py: implementation of different join functions

myCSV.py: load, preprocess, and preprocess CSV function

mybtree.py: build, load and store btree

select_and_print.py: print and output result of query

--------------------------------------------------------------------------------------------------------------------

How to use this system

run Terminal.py in terminal to start, -f for file name, -p for path that stores the Btree file
    for example, python3.6 Terminal.py -f review.csv photos.csv business.csv -p btree100/

The code will display the attributes for the selected file, and then prompt the following options:
1. Preprocess
2. Read in total
3. Build index
4. Run Query
5. Exit


\1. Preprocess, split the CSV file

\2. Read in total, use CSV file without split

\3. Build in index, build index for selected attribute, in the format of csv file name, attribute name, y/n(is numeric or not)
   for example, review.csv funny y
   
\4. Run query, query example:
  
  Q1: SELECT R.review_id, R.funny, R.useful FROM review.csv R WHERE R.funny >= 20 AND R.useful > 30
  
  Q2: SELECT B.name, B.city, B.state FROM business.csv B WHERE B.city = 'Champaign' AND B.state = 'IL'
  
  Q3: SELECT B.name, B.postal_code, R.stars, R.useful FROM business.csv B, review.csv R WHERE B.business_id = R.business_id AND B.name = 'Sushi Ichiban' AND B.postal_code = '61820'
  
  Q4: SELECT R1.user_id, R2.user_id, R1.stars, R2.stars FROM review.csv R1, review.csv R2 WHERE R1.business_id = R2.business_id AND R1.stars = 5 AND R2.stars = 1 AND R1.useful > 50 AND R2.useful > 50
  
  Q5: SELECT B.name, B.city, B.state, R.stars, P.label FROM business.csv B, review.csv R, photos.csv P WHERE B.business_id = R.business_id AND B.business_id = P.business_id AND B.city = 'Champaign' AND B.state = 'IL' AND R.stars = 5 AND P.label = 'inside'
  
  Q6: SELECT B.name, R1.user_id, R2.user_id FROM business.csv B, review.csv R1, review.csv R2 WHERE B.business_id = R1.business_id AND R1.business_id = R2.business_id AND R1.stars = 5 AND R2.stars = 1 AND R1.useful > 50 AND R2.useful > 50
  
\5. Exit


