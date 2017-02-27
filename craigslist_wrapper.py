import csv
from craigslist import CraigslistHousing
import codecs


zipcodes = [94110, 94107, 94103, 94114]

results = {}
keys = []

for zipcode in zipcodes:
	cl_h = CraigslistHousing(site='sfbay', area='sfc',
                         filters={'min_price': 4000, 'max_price': 6200, 'bedrooms': 3, 'bathrooms': 2, 'zip_code': zipcode})
	results[zipcode] = list(cl_h.get_results(sort_by='newest', geotagged=True))
	keys = results[zipcode][0].keys()

keys.append('lat')
keys.append('long')
with open('results.csv', 'wb') as csv_file:
	wr = csv.DictWriter(csv_file, keys)
	wr.writeheader()
	for zip in results.keys():
		for result in results[zip]:
			print(result)
			result['name'] = ''

			geotag = result['geotag']
			if geotag is not None:
				lat = geotag[0]
				long = geotag[1]
				result['lat'] = lat
				result['long'] = long
			
			wr.writerow(result)

 	
'''
{'name': u'3bd/2ba/1pk Remolded/Furnished Noe Flat', 
'has_image': True, 'url': u'http://sfbay.craigslist.org/sfc/apa/6012772248.html', 
'has_map': True, 'price': u'$6000', 'geotag': (37.7587, -122.433), 
'where': u'noe valley', 'id': u'6012772248', 'datetime': u'2017-02-25 12:35'}
'''