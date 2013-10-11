#!/usr/bin/env python
import sys
import math
# INSTRUCTIONS !
# The provided code calculates phi coefficients for each code line.
# Make sure that you understand how this works, then modify the provided code
# to work also on function calls (you can use your code from problem set 5 here)
# Use the mystery function that can be found at line TODO 170 and the
# test cases at line TODO 165 for this exercise.
# Remember that for functions the phi values have to be calculated as
# described in the problem set 5 video -
# you should get 3 phi values for each function - one for positive values (1),
# one for 0 values and one for negative values (-1), called "bins" in the video.
#
# Then combine both approaches to find out the function call and its return
# value that is the most correlated with failure, and then - the line in the
# function. Calculate phi values for the function and the line and put them
# in the variables below.
# Do NOT set these values dynamically.

answer_function = "f5"   # One of f1, f2, f3
answer_bin = 42          # One of 1, 0, -1
answer_function_phi = 42.0000    # precision to 4 decimal places.
answer_line_phi = 42.0000  # precision to 4 decimal places.
# if there are several lines with the same phi value, put them in a list,
# no leading whitespace is required
answer_line = ["if False:", 'return "FAIL"']  # lines of code


# These are the input values you should test the mystery function with
inputs = ["aaaaa223%", "aaaaaaaatt41@#", "asdfgh123!", "007001007", "143zxc@#$ab", "3214&*#&!(", "qqq1dfjsns", "12345%@afafsaf"]

###### MYSTERY FUNCTION

def mystery(magic):
    assert type(magic) == str
    assert len(magic) > 0

    r1 = f1(magic)

    r2 = f2(magic)

    r3 = f3(magic)

    # print magic, r1, r2, r3

    if r1 < 0 or r3 < 0:
        return "FAIL"
    elif (r1 + r2 + r3) < 0:
        return "FAIL"
    elif r1 == 0 and r2 == 0:
        return "FAIL"
    else:
        return "PASS"


def f1(ml):
    if len(ml) <6:
        return -1
    elif len(ml) > 12:
        return 1
    else:
        return 0

def f2(ms):
    digits = 0
    letters = 0
    for c in ms:
        if c in "1234567890":
            digits += 1
        elif c.isalpha():
            letters += 1
    other = len(ms) - digits - letters
    grade = 0

    if (other + digits) > 3:
        grade += 1
    elif other < 1:
        grade -= 1

    return grade

def f3(mn):
    forbidden = ["pass", "123", "qwe", "111"]
    grade = 0
    for word in forbidden:
        if mn.find(word) > -1:
            grade -= 1
    if mn.find("%") > -1:
        grade += 1
    return grade

# global variable to keep the coverage data in
coverage = {}  # :: f_name -> bin(-1,0,1) -> [r_val]
# Tracing function that saves the coverage data
# To track function calls, you will have to check 'if event == "return"', and in
# that case the variable arg will hold the return value of the function,
# and frame.f_code.co_name will hold the function name
fun_to_trace = ["f1","f2","f3"]
def traceit(frame, event, arg):
    global coverage   # :: f_name -> bin(-1,0,1) -> [r_val]

    f_name = frame.f_code.co_name  # function name
    if event == "return" and f_name in fun_to_trace:
        r_val = arg  # return value
        r_category = categorize(r_val)

        if f_name not in coverage:
            coverage[f_name] = {}
        # if r_category not in coverage[f_name]:
        #     coverage[f_name][r_category] = []
        coverage[f_name][r_category] = True

    return traceit

def categorize(r_val):
    """
    return value r_category
    =======================
    bin | meaning           | numeric | bool  | string   |special vaule
    ---------------------------------------------------------
    -1  | less than zero    | n<0     |       |          |None,NaN,Excptions
    0   | zero              | n=0     | False | len(n)=0 |
    1   | greater than zero | n>0     | True  | len(n)>0 |
    """
    if r_val is True:
        r_category = 1
    elif r_val is False:
        r_category = 0
    elif isinstance(r_val, (int, long, float, complex)):
        if r_val < 0:
            r_category = -1
        elif r_val == 0:
            r_category = 0
        else:
            r_category =1
    elif type(r_val) is str:
        r_category = 0 if len(r_val)==0 else 1
    else:
        r_category = -1
    return r_category

# Calculate phi coefficient from given values
def phi(n11, n10, n01, n00):
    return ((n11 * n00 - n10 * n01) /
            math.sqrt((n10 + n11) * (n01 + n00) * (n10 + n00) * (n01 + n11)))

# Print out values of phi, and result of runs for each covered line
def eval_print_table(tables):
    for f_name in tables:
        for bin in tables[f_name]:
            (n11, n10, n01, n00) = tables[f_name][bin]
            try:
                factor = phi(n11, n10, n01, n00)
                prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
            except:
                prefix = "       %2d%2d%2d%2d" % (n11, n10, n01, n00)
            # factor = phi(n11, n10, n01, n00)
            # prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
            print prefix, f_name, bin

# Run the program with each test case and record
# input, outcome and coverage of lines
def run_tests(inputs):
    runs   = []
    for input in inputs:
        global coverage
        coverage = {}

        sys.settrace(traceit)
        outcome = mystery(input)
        sys.settrace(None)

        runs.append((input, outcome, coverage))
    return runs

# Create empty tuples for each covered line
def init_tables(runs):
    tables = {}
    for (input, outcome, coverage) in runs:
        for f_name,bins in coverage.iteritems():
            for bin in bins.keys():
                if f_name not in tables:
                    tables[f_name] = {}
                if bin not in tables[f_name]:
                    tables[f_name][bin] = (0, 0, 0, 0)

    return tables

# Compute n11, n10, etc. for each line
def compute_n(tables):
    for f_name, bins in tables.iteritems():
        for bin in bins.keys():
            (n11, n10, n01, n00) = tables[f_name][bin]
            for (input, outcome, coverage) in runs:
                if f_name in coverage and bin in coverage[f_name]:
                    # Covered in this run
                    if outcome == "FAIL":
                        n11 += 1  # covered and fails
                    else:
                        n10 += 1  # covered and passes
                else:
                    # Not covered in this run
                    if outcome == "FAIL":
                        n01 += 1  # uncovered and fails
                    else:
                        n00 += 1  # uncovered and passes
            tables[f_name][bin] = (n11, n10, n01, n00)
    return tables

# Now compute (and report) phi for each line. The higher the value,
# the more likely the line is the cause of the failures.

runs = run_tests(inputs)

tables = init_tables(runs)

tables = compute_n(tables)

eval_print_table(tables)

import pprint
pp = pprint.PrettyPrinter(indent=4)
print "------------tables------------"
pp.pprint(tables)
print "------------runs------------"
pp.pprint(runs)
