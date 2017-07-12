import loaddata as ld
import csv

tournsum, field, setup = ld.loadhistoricaldata()

tourneylist = []
for key in tournsum.keys():
        for shortname in tournsum[key].keys():
                for year in tournsum[key][shortname].keys():
                        for plyr in tournsum[key][shortname][year]['players'].keys():
                                tourneylist.append([key, shortname, year, plyr,\
                                tournsum[key][shortname][year]['players'][plyr]['finposvalue'],\
                                tournsum[key][shortname][year]['players'][plyr]['primarytour'],\
                                tournsum[key][shortname][year]['players'][plyr]['name'],\
                                tournsum[key][shortname][year]['players'][plyr]['money'],\
                                tournsum[key][shortname][year]['players'][plyr]['finposnum'],\
                                tournsum[key][shortname][year]['players'][plyr]['totalscore'],\
                                tournsum[key][shortname][year]['players'][plyr]['eventfedexpoints'],\
                                tournsum[key][shortname][year]['players'][plyr]['plyrname'],\
                                tournsum[key][shortname][year]['players'][plyr]['relparscrtot']])

with open('tabledata/tournamenttable_plyr.txt', 'w') as f:
	#f.writelines("%s\n" % item for item in tourneylist)
	csv_writer = csv.writer(f)
	csv_writer.writerows(tourneylist)

import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='pga')

cursor = mydb.cursor()

csv_data = csv.reader(file('tabledata/tournamenttable_plyr.txt'))
for row in csv_data:
	print row
	cursor.execute('insert into tournsum(t_id, shortname, year, plyr_id,\
	finposvalue, primarytour, plyr_name, money, finposnum, totalscore,\
	eventfedexpoints, plyr_name_last_first, relparscrtot) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', row)
  
#close the connection to the database.
mydb.commit()
cursor.close()
print "Done"
