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

# TODO: It might save some hardship and be faster to use numpy 
# to get matrix functions (especially inverse which I'm going to need)

# Takes in a matrix as a list of lists and returns its transpose
def transpose(matrix):
	num_cols = len(matrix[0])
	cols = list()
	for i in range(num_cols):
		cols.append(list())

	for row in matrix:
		if(len(row) != num_cols):
			print "All rows must be the same size!!"
			return

		for i in range(len(row)):
			cols[i].append(row[i])

	return cols

###########################################################

# Takes in a list of data and normalize it
def normalize_list(input_list):
	output_list = list()

	return output_list

###########################################################

# Takes in a list of rows (lists) and normilizes it
# by columns (same index in each list). We require that
# the input be a matrix, ie every row has the same length
def normalize_data(matrix):
	output = transpose(matrix)
	return output

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



		numpy_example(data)



		#print data
		#data = normalize_data(data)
		#print data

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