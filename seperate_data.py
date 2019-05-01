import csv
import argparse

# https://docs.python.org/2/library/csv.html
# using examples for csv to open file
def read_csv(filename):
	with open(filename, 'rb') as csvfile:
		spamreader = csv.reader(csvfile)

		first = True

		cols = list()
		for row in spamreader:
			if(first):
				if(args.get("print_headers")):
					print row
					return

				cols = get_cols_from_headers(row)
				first = False

			if(args.get("print_data")):
				print_row = list()
				for i in range(len(row)):
					if(cols.count(i) != 0):
						print_row.append(row[i])

				print print_row


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Seperate data")
	parser.add_argument("--data_file",
											metavar="data_file.csv",
											help="Path to data file to read",
											required=True)
	
	parser.add_argument("--training_data_file",
											metavar="training_data.csv",
											help="Path used to write out training data",
											required=True)

	parser.add_argument("--tuning_data_file",
											metavar="tuning_data.csv",
											help="Path used to write out tuning data",
											required=True)

	parser.add_argument("--validation_data_file",
											metavar="validation_data.csv",
											help="Path used to write out validation data",
											required=True)

	parser.add_argument("--training_percent",
											metavar="70",
											help="Percent of data to use for training",
											type=float,
											default=70)

	parser.add_argument("--tuning_percent",
											metavar="10",
											help="Percent of data to use for tuning",
											type=float,
											default=10)

	parser.add_argument("--validation_percent",
											metavar="20",
											help="Percent of data to use for validation",
											type=float,
											default=20)

	args = vars(parser.parse_args())


	read_csv(args.get("data_file"))