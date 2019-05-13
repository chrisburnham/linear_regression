# Chris Burnham
# VTC Machine Learning 2019


import csv
import argparse
import random

###########################################################

# Cleans the data in our generated lists
def clean_lists(train_list, tune_list, validate_list):
	clean_data(train_list)
	clean_data(tune_list)
	clean_data(validate_list)

###########################################################

# Cleans the data to all be convertable to a float
# Note this is likely only useful for kc_house_data.csv
# Clean the data contained in the list
def clean_data(data_list):
	for i in range(len(data_list)):
		for j in range(len(data_list[i])):
			# Removing T and time from dates
			if(data_list[i][j].count('T') == 1):
				split_list = data_list[i][j].split('T')
				data_list[i][j] = float(split_list[0])

###########################################################

# Write a list of rows to a CSV
def write_csv(filename, list):
	with open(filename, 'wb') as csvfile:
		csv_writer = csv.writer(csvfile)
		for row in list:
			csv_writer.writerow(row)

###########################################################

# Recursive function to sperate out the source data
# into training, tuning, and validation CSV files.
# If random break down does not meet the tolerance 
# we try again unless we have taken more than
# max_attempts attempts at it already
def seperate_csv(filename, attempts):
	attempts += 1
	if(attempts > args.get("max_attempts")):
		print "Too many attempts. Giving up"
		return


	train_percent = args.get("training_percent")
	tune_percent = args.get("tuning_percent")
	validate_percent = args.get("validation_percent")

	if((train_percent < 0) or (tune_percent < 0) or (validate_percent < 0)):
		print "Percents must be positive"
		return

	if((train_percent + tune_percent + validate_percent) > 100):
		print "Total percent cannot exceed 100"
		return

	rand = random.Random()
	rand.seed()

	train_list = list()
	tune_list = list()
	validate_list = list()
	num_skipped = 0.0
	total_rows = 0.0

	with open(filename, 'rb') as csvfile:
		csv_reader = csv.reader(csvfile)

		for row in csv_reader:
			total_rows += 1.0

			# Want headers in all our CSV's
			if(total_rows == 1.0): # TODO: this should really be a fuzzy compare
				train_list.append(row)
				tune_list.append(row)
				validate_list.append(row)
				continue

			rand_num = rand.uniform(0, 100)
			if(rand_num < train_percent):
				train_list.append(row)
			elif(rand_num < (train_percent + tune_percent)):
				tune_list.append(row)
			elif(rand_num < (train_percent + tune_percent + validate_percent)):
				validate_list.append(row)
			else:
				num_skipped += 1.0

	train_actual = 100 * (len(train_list) / total_rows)
	tune_actual = 100 * (len(tune_list) / total_rows)
	validate_actual = 100 * (len(validate_list) / total_rows)
	skip_actual = 100 * (num_skipped / total_rows)

	print "Acutual Percents:"
	print "Training: ", train_actual, "%"
	print "Tuning:   ", tune_actual, "%"
	print "Validate: ", validate_actual, "%"
	print "Skipped:  ", skip_actual, "%"

	tolerance = args.get("percent_tolerance")
	if((abs(train_percent - train_actual) > tolerance) or
		 (abs(tune_percent - tune_actual) > tolerance) or
		 (abs(validate_percent - validate_actual) > tolerance)):
		print "Percents outside of tolerance. Trying again"
		seperate_csv(filename, attempts)
		return

	if(args.get("clean_data")):
		print "Cleaning data"
		clean_lists(train_list, tune_list, validate_list)

	write_csv(args.get("training_data_file"), train_list)
	write_csv(args.get("tuning_data_file"), tune_list)
	write_csv(args.get("validation_data_file"), validate_list)
	print "CSV's written!"

###########################################################

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

	parser.add_argument("--percent_tolerance",
											metavar="1",
											help="How close to the specified percents do we need to be",
											type=float,
											default=1)

	parser.add_argument("--max_attempts",
											metavar="10",
											help="How times do we try to fulfil our tolerance before we give up",
											type=int,
											default=10)

	parser.add_argument("--clean_data",
											action="store_true",
											help="Clean data so it can be interpreted as floats")

	args = vars(parser.parse_args())

	seperate_csv(args.get("data_file"), 0)