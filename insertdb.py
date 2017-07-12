import loaddata as ld
import csv

tournsum, field, setup = ld.loadhistoricaldata()

tourneylist = []
for key in tournsum.keys():
	for shortname in tournsum[key].keys():
		for year in tournsum[key][shortname].keys():
			tourneylist.append([key, shortname, year, tournsum[key][shortname][year]['tournamentname']])

with open('tabledata/tournamenttable.txt', 'w') as f:
	#f.writelines("%s\n" % item for item in tourneylist)
	csv_writer = csv.writer(f)
	csv_writer.writerows(tourneylist)

import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='pga')

cursor = mydb.cursor()

csv_data = csv.reader(file('tabledata/tournamenttable.txt'))
for row in csv_data:
	print row
	cursor.execute('insert into tournaments(t_id, name, year, fullname) values(%s,%s,%s,%s)', row)
  
#close the connection to the database.
mydb.commit()
cursor.close()
print "Done"
