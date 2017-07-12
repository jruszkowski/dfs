import urllib2
from bs4 import BeautifulSoup

field = "http://www.pgatour.com/data/r/"
filedirectory = 'historicaldata/'
jsonfiles = ['setup', 'tournsum', 'teetimes', 'course', 'field']

def getjson(page):
    page = urllib2.urlopen(page)
    soup = BeautifulSoup(page)
    return soup.get_text()

tourneyids = ['490']

years = list(range(2000,2018))

for tourneyid in tourneyids:
    for year in years:
        for json in jsonfiles:
            try:
		print field+tourneyid+'/'+str(year)+'/' + json + '.json'
                jsondata = getjson(field+tourneyid+'/'+str(year)+'/' + json + '.json')
                if len(jsondata) > 0:
                    with open(filedirectory+tourneyid+'_' + str(year) + '_' + json + '.txt', 'w') as f:
                        f.write(jsondata)
            except:
		print 'no good', tourneyid
                continue


