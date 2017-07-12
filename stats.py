import urllib2
from bs4 import BeautifulSoup
from unicodedata import normalize
import MySQLdb
import scrape_field
import pandas as pd

shortname = 'John Deere Classic'

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='pga')

cursor = mydb.cursor()

query = ("select plyr_name, totalscore, finposnum from tournsum where year = 2016 and shortname = '%s';" % shortname)
cursor.execute(query)

past_results = {}
for x,y,z in cursor:
	if z < 999:
		past_results[x] = int(y)
	elif z == 999 and y > 120 and y < 190:
		past_results[x] = max(300, int(y) * 2)
	elif z == 999 and y >= 190 and y < 240:
		past_results[x] = int(y) * 4/3.

#close the connection to the database.
#mydb.commit()
cursor.close()
mydb.close()

stats = {
103: 'GIR',
111: 'SAND',
119: 'PUTTS',
120: 'SCORE',
138: 'TOP10',
145: 'PUTT3',
146: 'PUTT3_20',
147: 'PUTT3_25',
187: 'PRESIDENTS',
213: 'FAIRWAY',
214: 'D300',
215: 'D280',
216: 'D260',
217: 'D240',
218: 'D220',
326: 'GIR_200',
327: 'GIR_175',
328: 'GIR_150',
329: 'GIR_125',
330: 'GIR_100',
351: 'HOLE_OUT',
352: 'BIRD',
459: 'LEFT',
460: 'RIGHT',
461: 'MISSED'
}

def createdict(page):
   dict_page = {}
   page = urllib2.urlopen(page)
   soup = BeautifulSoup(page, "html5lib")
   right_table = soup.find('table', class_='table-styled')
   for row in right_table.findAll("tr"):
       cells = row.findAll('td')
       if len(cells) == 8:
           dict_page[cells[2].a.get_text()] = float(cells[4].string)
   dict_page = {normalize('NFKC', k): v for k, v in dict_page.items()}
   return dict_page


def createplyrlist(page):
   plyrlist = []
   page = urllib2.urlopen(page)
   soup = BeautifulSoup(page, "html5lib")
   right_table = soup.find('table', class_='table-styled')
   for row in right_table.findAll("tr"):
       cells = row.findAll('td')
       if len(cells) == 8:
           plyrlist.append(cells[2].a.get_text())
   return plyrlist

past_results = {unicode(k): v for k,v in past_results.items()}

listofstats = []
pagename = "http://www.pgatour.com/stats/stat."
pagenameend = ".2016.html"
df = pd.DataFrame.from_dict(past_results, orient='index')

for i in stats.keys():
   page = pagename + str(i) + pagenameend
   try:
       df[i] = pd.DataFrame.from_dict(createdict(page), orient='index')
       listofstats.append(i)
   except:
       print stats[i], i, ' No good'
       continue

df = df.corr()
df = df[0]
df.to_csv('corr.csv')

ind_var = [120, 218, 145, 459, 352]

df = pd.DataFrame.from_dict(past_results, orient='index')
for stat in ind_var:
   page = pagename + str(stat) + pagenameend
   try:
       df[stats[stat]] = pd.DataFrame.from_dict(createdict(page), orient='index')
   except:
       print stats[stat], 'No good'
       continue

import statsmodels.formula.api as sm

df = df.rename(columns={0:'Result'})
result = sm.ols(formula="Result ~ SCORE + D220 + PUTT3 + LEFT + BIRD", data=df).fit()
print result.params
print result.summary()

def get_predicted_score():
	new_field = []
	new_field_dict = scrape_field.field_dictionary()
	for key in new_field_dict.keys():
		for plyr in new_field_dict[key]['players'].keys():
			new_field.append(plyr)
	new_field = [x.split(',')[1].strip() + ' ' + x.split(',')[0] for x in new_field]
		
	df2017 = pd.DataFrame(new_field)
	df2017 = df2017.rename(columns={0: 'PredictedScore'})
	df2017 = df2017.set_index('PredictedScore')
	pagename = "http://www.pgatour.com/stats/stat."
	pagenameend = ".html"

	for stat in ind_var:
	   page = pagename + str(stat) + pagenameend
	   try:
	       df2017[stats[stat]] = pd.DataFrame.from_dict(createdict(page), orient='index')
	   except:
	       print stats[stat], 'No good'
	       continue

	df2017[2016] = 259.6808 + 0.1576 * df2017['SCORE'] + 2.7378 * df2017['D220'] + 2.1570 * df2017['PUTT3'] + 1.7851 * df2017['LEFT'] + -1.5529 * df2017['BIRD']
	df = df2017[2016]
	df.to_csv('johndeere.csv')
	
	return df.to_dict()


