



sql_statement = "SELECT movie_title, director_name FROM movies.csv WHERE country = English"

sql_statement = "SELECT movie_title, director_name FROM movies.csv WHERE country = English and title_year = 2008"

sql_statement = "SELECT * FROM movies.csv WHERE country = English"

sql_statement = "SELECT M1.movie_title, M2.movie_title, M1.director_name FROM movies.csv M1, movies.csv M2 WHERE M1.director_name = M2.director_name"

sql_statement = "SELECT M1.director_name, M1.movie_title, M1.title_year, M2.movie_title, M2.title_year FROM movies.csv M1, movies.csv M2 WHERE M1.director_name = M2.director_name and M1.title_year<M2.title_year"

sql_statement = "SELECT M1.director_name, M1.movie_title, M1.title_year, M2.movie_title, M2.title_year FROM movies.csv M1, movies.csv M2 WHERE M1.director_name = M2.director_name and M1.title_year<2009 and M2.title_year>=2010"

sql_statement = "SELECT M1.director_name, M1.movie_title, M2.movie_title, M3.movie_title FROM movies.csv M1, movies.csv M2, movies.csv M3 WHERE M1.director_name = M2.director_name and M1.director_name = M3.director_name and M1.budget > M2.budget and M2.budget > M3.budget"

sql_statement = "SELECT M1.director_name, M1.movie_title, M2.movie_title, M3.movie_title FROM movies.csv M1, movies.csv M2, movies.csv M3 WHERE M1.director_name = M2.director_name and M1.director_name = M3.director_name and M1.budget*1.5 > M2.budget and M2.budget >= M3.budget*1.5"

sql_statement = "SELECT M.movie_title, M.director_name, A.date, A.useful, A.cool FROM movies.csv M, review_500k.csv A"