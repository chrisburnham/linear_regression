import csv
import argparse
import numpy

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
# Matrix is all the possible columns to use to do this regression
# Results is a vector of the results we are attempting to predict
# Max_cols is the most columns we will try to find our best regression
# l is the lambda value we are using in our cost function
def find_best_regression(matrix, results, max_cols, l):

	# TODO: untested
	# TODO: What do we want to print/ return about this regression

	lowest_error = 9999999.9
	for i in range(max_cols):
		pass
		# TODO: loop through all varients of this number of cols
		# Do the regression, then calculate its error
		# use the error, i (number of cols), and lamba to calculate cost
		# if it is lower than what we currently have save the cost
		# and the regression


###########################################################

# Do a regression using the given data
# Matrix is the columns used to train (no leading ones needed)
# Results is a vector of the actual values we are trying to predict
# Returns a vector of the weights used for this regression
def regression(matrix, results):

	# TODO: untested

	# TODO: Add a column of 1's to matrix
	matrix_trans = matrix.transpose()
	try:
		inverted = numpy.linalg.inv(matrix_trans * matrix)
	except numpy.linalg.LinAlgError:
		print "Matrix times transpose not invertable"
	else:
		return (inverted * matrix_trans) * results

###########################################################

# Calculate the error for a regression
# Matrix of data used in regression
# Vector of results from regression
# Vector of calculated weights from regression
# Returns the average error
def regression_error(matrix, results, weights):

	# TODO: untested

	error = 0.0
	for i in range(matrix.shape[0]):
		prediction = predict_value(matrix[i,:], weights)
		diff = prediction - results[i]
		error += diff ** 2


###########################################################

# Predict a value based off of a row of input data
# Row of data to use
# Calculated regression weights
# Value we predict
def predict_value(input_data, weights):

	#TODO: untested
	output = weights[0, 0]
	for i in range(input_data.shape[1]):
		output += input_data[0, i] * weights[0, i+1]

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

def numpy_example(data):
	# Numpy examples I'm going to need
	nmatrix = numpy.matrix(data)

	print nmatrix
	trans = nmatrix.transpose()
	print trans


	print "\nInverse example"
	nmatrix2 = numpy.matrix([[2, 0],[0,2],[1,1]], dtype='f')

	try:
		inverse = numpy.linalg.inv(nmatrix2)
	except numpy.linalg.LinAlgError:
		print "Not invertable"
		pass
	else:
		print inverse

	print nmatrix2[:,0]
	print nmatrix2[1,:]

	print numpy.std(nmatrix2[:,0])
	print numpy.mean(nmatrix2[1,:])

	print "\nmanipulation"
	print nmatrix2
	nmatrix2[:,1] = nmatrix2[:,1] / 1.5
	print nmatrix2

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

#TODO: How do we merge/ add columns to a matrix

		#train_data = data_matrix[:,0:2].merge(data_matrix[:,4:] )
		#print train_data


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
											help="Columns to look at. Specify multiple times")

	parser.add_argument("--print_headers",
											action="store_true",
											help="Print headers and quit")

	parser.add_argument("--print_data",
											action="store_true",
											help="Print data specified")

	args = vars(parser.parse_args())


	read_csv(args.get("data_file"))