import dataset
import csv

db = dataset.connect('postgresql://shreyas@localhost:5455/sf_housing')


with open('results.csv', 'r') as csv_file:
	reader = csv.DictReader(csv_file)
	for row in reader:
		print(row)
		price = int(row.get('price', 0)[1:].replace(',', ''))


		db['house_list'].insert({
			'has_image': row['has_image'],
			'url': row['url'],
			'has_map': row['has_map'],
			'price': price,
			'geotag': row.get('geotag', 'none'),
			'where': row['where'],
			'house_list_id': row['id'],
			'datetime': row['datetime'],
			'lat': row.get('lat', 'none'),
			'long': row.get('long', 'none')
		})
2