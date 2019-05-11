import csv
import argparse
import numpy
import itertools

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


# Calculating a regression
# A = matrix of the values (with a leading column of 1's)
# w = vector of the weights for the regression
# y = matrix of the results (maybe a vector actually?)
# using A' to mean A transpose
# using A^-1 to mean A inverse
# w = (A'A)^-1A'y
# A transpose times A inverted. Times A transpose, with the inputs as its input


# Calculate error
# Sum of the squares of the errors (probably just sum the elements individually)

# Want to calc error for all possible varients of a given number of cols
# and pick the smallest error. Then if doing a range of number of colums
# we want to use a lambda to pick one (lowest cost). 
# cost = error + lambda * num_cols
# lambda and max cols (mabe min too) should be args

# lambda decided based off of tuning

# Want some sort of validation function. Probably calculate error on a function

###########################################################

# Find the lowest cost regression for this data
# Matrix is all the possible columns to use to do this regression (no leading ones)
# Results is a vector of the results we are attempting to predict
# Max_cols is the most columns we will try to find our best regression
# l is the lambda value we are using in our cost function
def find_best_regression(matrix, results, max_cols, l):

	# TODO: untested
	# TODO: What do we want to print/ return about this regression

	debug = True

	if(debug):
		print matrix
		print results

	lowest_cost = 9999999.9
	best_weights = list()
	best_cols = list()
	for i in range(min(max_cols, matrix.shape[1])):
		col_combos = itertools.combinations(range(matrix.shape[1]), i+1)
		for col_list in col_combos:

			if(debug):
				print "\nRegression:"
				print "Cols:"
				print col_list

			trimmed_matrix = numpy.zeros(shape=(matrix.shape[0], 1))
			trimmed_matrix.fill(1)
			for j in col_list:
				trimmed_matrix = numpy.c_[trimmed_matrix, matrix[:, j]]

			if(debug):
				print "Input data:"
				print trimmed_matrix

			weights = regression(trimmed_matrix, results)

			if(weights == None):
				print "bad regression"
				break;

			if(debug):
				print "Output weights:"
				print weights

			error = regression_error(trimmed_matrix, results, weights)

			if(debug):
				print "Error:"
				print error


			cost = (i * l) + error

			if(debug):
				print "Cost:"
				print cost
				print "\n"

			if(cost < lowest_cost):
				print "lower cost"
				lowest_cost = cost
				best_weights = weights
				best_cols = col_list

	print "\nBest Weights:"
	print best_weights
	print "on cols"
	print best_cols


###########################################################

# Do a regression using the given data
# Matrix is the columns used to train with leading column of ones
# Results is a vector of the actual values we are trying to predict
# Returns a vector of the weights used for this regression
def regression(matrix, results):
	matrix_trans = matrix.transpose()

	try:
		inverted = numpy.linalg.inv(matrix_trans * matrix)
	except numpy.linalg.LinAlgError:
		print "Matrix times transpose not invertable"
		print matrix_trans * matrix
	else:
		return (inverted * matrix_trans) * results

###########################################################

# Calculate the error for a regression
# Matrix of data used in regression with a leading 1 column
# Vector of results from regression
# Vector of calculated weights from regression
# Returns the error
def regression_error(matrix, results, weights):

	# TODO: untested

	error = 0.0
	for i in range(matrix.shape[0]):
		prediction = predict_value(matrix[i,:], weights)
		diff = prediction - results[i]
		error += diff ** 2

	return error


###########################################################

# Predict a value based off of a row of input data
# Row of data to use (includes leading 1)
# Calculated regression weights (column)
# Value we predict
def predict_value(input_data, weights):

	#TODO: untested
	output = 0

	for i in range(input_data.shape[1]):
		output += input_data[0, i] * weights[i, 0]

	return output

###########################################################

# Takes in a numpy matrix and normilizes it by column
def normalize_data(matrix):
	for i in range(matrix.shape[1]):
		mean = numpy.mean(matrix[:,i])
		std_dev = numpy.std(matrix[:,i])
		if(std_dev == 0):
			matrix[:,i] = 0
		else:
			matrix[:,i] = (matrix[:,i] - mean) / std_dev

###########################################################

def read_csv(filename):
	with open(filename, 'rb') as csvfile:
		csv_reader = csv.reader(csvfile)

		first = True

		cols = list()
		data = list()
		for row in csv_reader:
			if(first):
				if(args.get("print_headers")):
					print row
					return

				cols = get_cols_from_headers(row)

			data_row = list()
			for i in range(len(row)):
				if(cols.count(i) != 0):
					data_row.append(row[i])

			if(args.get("print_data")):
				print data_row

			if(not first):
				data.append(data_row)

			first = False

		data_matrix = numpy.matrix(data, dtype='f')
		normalize_data(data_matrix)

		train_data = numpy.c_[data_matrix[:,0:2], data_matrix[:,3:]]

		find_best_regression(train_data, data_matrix[:,2], 4, 0.01)



###########################################################

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run Linear Regression")

	parser.add_argument("--data_file",
											metavar="data_file.csv",
											help="Path to data file to read",
											required=True)

	parser.add_argument("-c",
											"--cols",
											action="append",
											metavar="Column_name",
											help="Columns to skip. Specify multiple times")

	parser.add_argument("--results",
											metavar="Column_name",
											help="Column with the the results")

	parser.add_argument("--print_headers",
											action="store_true",
											help="Print headers and quit")

	parser.add_argument("--print_data",
											action="store_true",
											help="Print data as we go")


	subparsers = parser.add_subparsers(help="Training or Validation")
	train_parser = subparsers.add_parser("train", help="Training arguments")
	train_parser.add_argument("--max_columns",
													  type=int,
													  metavar="num",
													  help="Max number of columns to look at")

	train_parser.add_argument("-l",
													  "--lambda",
													  type=float,
													  metavar="num",
													  help="Lambda value to choose the best regression")


	validate_parser = subparsers.add_parser("validate", help="Validation arguments")
	validate_parser.add_argument("--model_file",
														   metavar="file",
														   help="File that contains the model to validate")


	args = vars(parser.parse_args())


	read_csv(args.get("data_file"))