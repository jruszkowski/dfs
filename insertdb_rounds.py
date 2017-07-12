import loaddata as ld
import csv

tournsum, field, setup = ld.loadhistoricaldata()

round1 = []
round2 = []
round3 = []
round4 = []
for key in tournsum.keys():
        for shortname in tournsum[key].keys():
                for year in tournsum[key][shortname].keys():
                        for plyr in tournsum[key][shortname][year]['players'].keys():
                                if 'rndscore' in tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1'].keys():
                                        round1.append([key, shortname, year, plyr,\
					1,
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['rndscore'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['relparscr'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['rndpos'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['cumparscr'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['coursenum']])

                                if 'rndscore' in tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2'].keys():
                                        round2.append([key, shortname, year, plyr,\
					2,
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['rndscore'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['relparscr'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['rndpos'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['cumparscr'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['coursenum']])

                                if 'rndscore' in tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3'].keys():
                                        round3.append([key, shortname, year, plyr,\
					3,
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['rndscore'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['relparscr'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['rndpos'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['cumparscr'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['coursenum']])

                                if 'rndscore' in tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4'].keys():
                                        round4.append([key, shortname, year, plyr,\
					4,
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['rndscore'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['relparscr'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['rndpos'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['cumparscr'],\
                                        tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['coursenum']])

rounds = {'R1':round1,'R2':round2,'R3':round3,'R4':round4}

for r in rounds.keys():
	with open('tabledata/'+r+'.txt', 'w') as f:
		#f.writelines("%s\n" % item for item in tourneylist)
		csv_writer = csv.writer(f)
		csv_writer.writerows(rounds[r])

import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='pga')

cursor = mydb.cursor()

for r in rounds:
	csv_data = csv.reader(file('tabledata/'+r+'.txt'))
	for row in csv_data:
		print row
		cursor.execute('insert into round_data(t_id, shortname, year, plyr_id,\
		rndnum, rndscore, relparscr, rndpos, cumparscr, coursenum) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', row)
  
#close the connection to the database.
mydb.commit()
cursor.close()
print "Done"
