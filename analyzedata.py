import loaddata as ld

tournsum, field, setup = ld.loadhistoricaldata()

#print {x for key in tournsum.keys() for x in tournsum[key].keys()}
import pandas as pd

tournament = 'Wells Fargo Championship'
#tournament = 'Valero Texas Open'

plyrlist = []
for key in tournsum.keys():
	if tournament in tournsum[key].keys():
		plyrlist += [tournsum[key][tournament][plyr]['name'] for plyr in tournsum[key][tournament].keys()]
		
plyrset = set(plyrlist)
df = pd.DataFrame(index = plyrset)

for key in tournsum.keys():
	try:
		if tournament in tournsum[key].keys():
			df[key] = pd.DataFrame.from_dict({tournsum[key][tournament][plyr]['name']: fltconv(tournsum[key][tournament][plyr]['totalscore'])\
				 for plyr in tournsum[key][tournament].keys() if tournsum[key][tournament][plyr]['finposnum']!='999'}, orient='index')
	except:
		continue

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
                                if tournsum[key][tournament][plyr]['finposnum']!=999:
                                        y1_cutlist.append(plyr)

	for key in [str(year2)]:
        	if tournament in tournsum[key].keys():
			for plyr in y1_cutlist:
				if tournsum[key][tournament][plyr]['finposnum']!=999:
					mcut_y2 += 1

			for plyr in tournsum[key][tournament].keys():
				if tournsum[key][tournament][plyr]['finposnum']!=999:
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

print sum(listofdeltas)/len(listofdeltas)

