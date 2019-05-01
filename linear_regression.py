import csv
import argparse

# Pass in first row to return a list of the header
# indexs that we care about. If cols is not set 
# return all of them
def get_cols_from_headers(row):
	cols = list()
	arg_cols = args.get("cols")

	if((type(arg_cols) != type(list())) or (len(arg_cols) == 0)):
		cols = range(len(row))
	else:
		for i in range(len(row)):
			for name in arg_cols:
				if(name == row[i]):
					cols.append(i)
					break

	return cols

# https://docs.python.org/2/library/csv.html
# using examples for csv to open file
def read_csv(filename):
	with open(filename, 'rb') as csvfile:
		spamreader = csv.reader(csvfile)

		first = True

		cols = list()
		for row in spamreader:
			if(first):
				cols = get_cols_from_headers(row)
				first = False

			for i in range(len(row)):
				if(cols.count(i) != 0):
					print row[i]


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run Linear Regression")
	parser.add_argument("--data_file",
											metavar="data_file.csv",
											help="Path to data file to read",
											required=True)
	parser.add_argument("--cols",
											action="append",
											metavar="Column_name",
											help="Columns to look at. Specify multiple times")

	# TODO: arg to print headers

	args = vars(parser.parse_args())


	read_csv(args.get("data_file"))