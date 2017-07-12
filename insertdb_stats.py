import stats 
import MySQLdb

score_dict = stats.get_predicted_score()
shortname = 'John Deere Classic'

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='pga')

cursor = mydb.cursor()
query = ("select distinct t_id from tournsum where shortname = '%s';" % shortname)
cursor.execute(query)
#close the connection to the database.
#mydb.commit()
cursor.close()

cursor = mydb.cursor()
for item in score_dict.items():
	row = '030', shortname, '2017', item[0], item[1]
	query = ('insert into pga.score_prediction(t_id, shortname, year, plyr_name,\
        p_score) values(%s, %s, %s, %s, %s);', row)
	print query
	cursor.execute(*query)
#close the connection to the database.
mydb.commit()
cursor.close()
mydb.close()
