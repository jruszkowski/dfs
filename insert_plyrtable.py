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
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['rndscore'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['relparscr'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['rndpos'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['cumparscr'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['coursenum']])

				if 'rndscore' in tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2'].keys():
					round2.append([key, shortname, year, plyr,\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['rndscore'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['relparscr'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['rndpos'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['cumparscr'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['coursenum']])

				if 'rndscore' in tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3'].keys():
					round3.append([key, shortname, year, plyr,\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['rndscore'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['relparscr'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['rndpos'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['cumparscr'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['coursenum']])

				if 'rndscore' in tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4'].keys():
					round4.append([key, shortname, year, plyr,\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['rndscore'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['relparscr'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['rndpos'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['cumparscr'],\
					tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['coursenum']])


maxlist1 = set([type(x[4]) for x in round1])
maxlist2 = set([type(x[5]) for x in round1])
maxlist3= max([len(x[6]) for x in round1])
maxlist4= set([type(x[7]) for x in round1])
maxlist5= max([len(x[8]) for x in round1])

print maxlist1, maxlist2, maxlist3, maxlist4, maxlist5 
int, int, char4, int, char3
