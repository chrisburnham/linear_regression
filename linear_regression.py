import csv
import argparse

# https://docs.python.org/2/library/csv.html
# using examples for csv to open file
def read_csv(filename):
	with open(filename, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in spamreader:
			print ', '.join(row)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run Linear Regression")
	parser.add_argument("--data_file",
											help="Path to data file to read",
											required=True)

	args = vars(parser.parse_args())

	read_csv(args.get("data_file"))