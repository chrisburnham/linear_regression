import csv

# https://docs.python.org/2/library/csv.html
# using examples for csv to open file
def read_csv(filename):
	with open(filename, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in spamreader:
			print ', '.join(row)


read_csv("kc_house_data.csv")