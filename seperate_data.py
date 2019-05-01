import csv
import argparse
import random

# https://docs.python.org/2/library/csv.html
# using examples for csv to open file
def seperate_csv(filename):
	train_percent = args.get("training_percent")
	tune_percent = args.get("tuning_percent")
	validate_percent = args.get("validation_percent")

	if((train_percent < 0) or (tune_percent < 0) or (validate_percent < 0)):
		print "Percents must be positive"
		return

	if((train_percent + tune_percent + validate_percent) > 100):
		print "Total percent cannot exceed 100"
		return

	with open(filename, 'rb') as csvfile:
		spamreader = csv.reader(csvfile)

		first = True

		cols = list()
		#for row in spamreader:




if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Seperate data")
	parser.add_argument("--data_file",
											metavar="data_file.csv",
											help="Path to data file to read",
											required=True)
	
	parser.add_argument("--training_data_file",
											metavar="training_data.csv",
											help="Path used to write out training data",
											default="training_data.csv")

	parser.add_argument("--tuning_data_file",
											metavar="tuning_data.csv",
											help="Path used to write out tuning data",
											default="tuning_data.csv")

	parser.add_argument("--validation_data_file",
											metavar="validation_data.csv",
											help="Path used to write out validation data",
											default="validation_data.csv")

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


	seperate_csv(args.get("data_file"))