import csv
import argparse

# https://docs.python.org/2/library/csv.html
# using examples for csv to open file
def read_csv(filename):
	with open(filename, 'rb') as csvfile:
		spamreader = csv.reader(csvfile)

		first = True

		# TODO: if we have no cols choose them all
		#if(len(args.get("cols")) == 0)
			#first 

		cols = list()
		for row in spamreader:
			if(first):
				for i in range(len(row)):
					for name in args.get("cols"):
						if(name == row[i]):
							cols.append(i)

				first = False

			for i in range(len(row)):
				# TODO: check if in cols


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run Linear Regression")
	parser.add_argument("--data_file",
											metavar="data_file.csv",
											help="Path to data file to read",
											required=True)
	parser.add_argument("--cols",
											action="append",
											metavar="Column_name",
											help="Columns to look at. Specify multiple times",
											required=True)

	# TODO: arg to print headers

	args = vars(parser.parse_args())


	read_csv(args.get("data_file"))