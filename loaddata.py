import os
import json

#filedirectory = 'historicaldata/'
filedirectory = 'testdir/'
filelist = os.listdir(filedirectory)

def e_utf(data):
	'''convert from unicode to string'''
	return data.encode("utf-8")

def intconv(data):
	'''convert blanks to zero'''
	if data.isdigit():
		return int(e_utf(data))
	else:
		return 0 

def rounddata(data):
	rounds = {'R1': {}, 'R2': {}, 'R3':{}, 'R4':{}}
	for r in data:
		print r
		if e_utf(r['rndNum']) == 'Round 1':
			rounds['R1'] = {'rndscore': intconv(r['rndScr']),\
			 'relparscr': intconv(r['relParScr']),\
			 'rndpos': e_utf(r['rndPos']),\
			 'cumparscr': intconv(r['cumParScr']),\
			 'coursenum': e_utf(r['courseNum'])}
                if e_utf(r['rndNum']) == 'Round 2':
                        rounds['R2'] = {'rndscore': intconv(r['rndScr']),\
                         'relparscr': intconv(r['relParScr']),\
                         'rndpos': e_utf(r['rndPos']),\
                         'cumparscr': intconv(r['cumParScr']),\
                         'coursenum': e_utf(r['courseNum'])}
                if e_utf(r['rndNum']) == 'Round 3':
                        rounds['R3'] = {'rndscore': intconv(r['rndScr']),\
                         'relparscr': intconv(r['relParScr']),\
                         'rndpos': e_utf(r['rndPos']),\
                         'cumparscr': intconv(r['cumParScr']),\
                         'coursenum': e_utf(r['courseNum'])}
                if e_utf(r['rndNum']) == 'Round 4':
                        rounds['R4'] = {'rndscore': intconv(r['rndScr']),\
                         'relparscr': intconv(r['relParScr']),\
                         'rndpos': e_utf(r['rndPos']),\
                         'cumparscr': intconv(r['cumParScr']),\
                         'coursenum': e_utf(r['courseNum'])}
	return rounds

tournsum = {}
for f in filelist:
	if f.split('_')[2].split('.')[0] == 'tournsum':
		year = f.split('_')[1]
		if year not in tournsum.keys():
			tournsum[year] = {}
		with open(filedirectory + f) as json_data:
			try: 
	    			d = json.load(json_data)
				for key in d.keys():
					if e_utf(key) == 'years':
						if e_utf(d[key][0]['tours'][0]['tourName']) == 'PGA TOUR':
							tournsum[year][e_utf(d[key][0]['tours'][0]['trns'][0]['shortName'])] = {}
							print d[key][0]['tours'][0]['trns'][0]['plrs'][0].keys()
							for plyr in d[key][0]['tours'][0]['trns'][0]['plrs']:
								tournsum[year][e_utf(d[key][0]['tours'][0]['trns'][0]['shortName'])][e_utf(plyr['plrNum'])] = \
								{'EventFedExPoints': intconv(plyr['EventFedExPoints']),\
								'Name': e_utf(plyr['name']['first'] + ' ' + plyr['name']['last']),\
								'totalscore': intconv(plyr['totScr']),\
								'primaryTour': e_utf(plyr['primaryTour']),\
								'finposnum': intconv(plyr['finPos']['finPosNum']),\
								'finposvalue': intconv(plyr['finPos']['finPosValue']),\
								'money': intconv(plyr['money'].replace(',','')),\
								'relparscrtot': intconv(plyr['relParScrTot']),\
								'rounddata': rounddata(plyr['rnds'])
								}
			except:
				continue
print tournsum
