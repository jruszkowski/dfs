import os
import json

filedirectory = 'historicaldata/'
#filedirectory = 'testdir/'
filelist = os.listdir(filedirectory)

def e_utf(data):
	'''convert from unicode to string'''
	return data.encode("utf-8")

def fltconv(data):
	'''convert blanks to zero'''
	if data.isdigit():
		return float(data)
	else:
		return 0 

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
							for plyr in d[key][0]['tours'][0]['trns'][0]['plrs']:
								tournsum[year][e_utf(d[key][0]['tours'][0]['trns'][0]['shortName'])][plyr['plrNum']] = \
								{'EventFedExPoints': plyr['EventFedExPoints'],\
								'Name': plyr['name']['first'] + ' ' + plyr['name']['last'],\
								'totalscore': plyr['totScr'],\
								'primaryTour': plyr['primaryTour'],\
								'primaryTour': plyr['primaryTour'],\
								'finposnum': plyr['finPos']['finPosNum'],\
								'finposvalue': plyr['finPos']['finPosValue'],\
								'money': plyr['money'].replace(',',''),\
								'relparscrtot': plyr['relParScrTot']
								}
			except:
				continue

#print {x for key in tournsum.keys() for x in tournsum[key].keys()}
import pandas as pd

#tournament = 'Wells Fargo Championship'
tournament = 'Valero Texas Open'

plyrlist = []
for key in tournsum.keys():
	if tournament in tournsum[key].keys():
		plyrlist += [tournsum[key][tournament][plyr]['Name'] for plyr in tournsum[key][tournament].keys()]
		
plyrset = set(plyrlist)

df = pd.DataFrame(index = plyrset)

for key in tournsum.keys():
	try:
		if tournament in tournsum[key].keys():
			df[key] = pd.DataFrame.from_dict({tournsum[key][tournament][plyr]['Name']: fltconv(tournsum[key][tournament][plyr]['totalscore'])\
				 for plyr in tournsum[key][tournament].keys() if tournsum[key][tournament][plyr]['finposnum']!='999'}, orient='index')
	except:
		continue

#df['Avg'] = (df['2016'] + df['2015']) / 2.
#print df[(df['2016']>0) & (df['2015']>0)].sort('Avg')

import collections

years = range(2000,2016)

def getcounts(year1, year2):
	plyrlist = []
	for key in [year1, year2]:
        	if tournament in tournsum[key].keys():
                	plyrlist += [plyr for plyr in tournsum[key][tournament].keys()]
	plyrcount = collections.Counter(plyrlist)
	plyd2years = []
	for x,y in plyrcount.items():
		if y == 2:
			plyd2years.append(x)
	return plyd2years

resultsdict = {}
while len(years) > 0:
 try:
	year1 = years.pop()
	year2 = year1 + 1
	plyd2years = getcounts(str(year1), str(year2))
	totalplyrs = len(plyd2years)
	mcut_y2 = 0
	t_y2 = 0
	t_mcut_y2 = 0
	y1_cutlist = []
	resultsdict[year1] = {}
	for key in [str(year1)]:
       		if tournament in tournsum[key].keys():
               		for plyr in plyd2years:
                                if tournsum[key][tournament][plyr]['finposnum']!='999':
                                        y1_cutlist.append(plyr)

	for key in [str(year2)]:
        	if tournament in tournsum[key].keys():
			for plyr in y1_cutlist:
				if tournsum[key][tournament][plyr]['finposnum']!='999':
					mcut_y2 += 1

			for plyr in tournsum[key][tournament].keys():
				if tournsum[key][tournament][plyr]['finposnum']!='999':
       	                                t_mcut_y2 += 1
					t_y2 += 1
				else:
					t_y2 += 1 

	resultsdict[year1] = {'2y': mcut_y2/float(len(y1_cutlist)), 'field': t_mcut_y2/float(t_y2)}
 except:
	continue
listofdeltas = []
for key in resultsdict.keys():
	if len(resultsdict[key]) > 0:
		difference = resultsdict[key]['2y'] - resultsdict[key]['field']
		listofdeltas.append(difference)

print sum(listofdeltas)/len(listofdeltas), resultsdict 


