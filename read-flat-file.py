#!/usr/bin/env python
# Make a delimited file easier to read
import argparse
import logging
import math
import os
import pwd
import re
import sre_constants
import sys
# Imports above are standard Python, imports below are Oppenheimer
import base
CR = chr(10)
TAB = chr(9)
DEFAULT_DELIMITER = ","

parser = argparse.ArgumentParser(description='', epilog='''
Read a character-delimited file. Input taken from specified file or STDIN if no file specified.
'''.format(**locals()))
parser.add_argument("input-file", nargs='?', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument("--delimiter", default=DEFAULT_DELIMITER, help="Default is '{DEFAULT_DELIMITER}'. Enclose in quotes.".format(**locals()))
parser.add_argument("--first-line-is-header", action="store_true", help="Cause the first line to be treated as column headers, not data.")
parser.add_argument("--regular-expression", metavar="PERL-COMPATIBLE", default=".", help="Enclose in quotes. Causes inclusion of only those rows that match the expression; the match is case-insensitive.".format(**locals()))
parser.add_argument("--verbose", action="store_true", help="Write more messages to STDERR.")
parser.add_argument("--terse", action="store_true", help="Write fewer messages to STDERR.")
parser.add_argument("--whoami", help=argparse.SUPPRESS, default=pwd.getpwuid(os.geteuid()).pw_name)
cmdline_arg_dict = parser.parse_args().__dict__
delimiter_char = cmdline_arg_dict["delimiter"]
header_flag = cmdline_arg_dict["first_line_is_header"]
reg_exp = cmdline_arg_dict["regular_expression"]
whoami = cmdline_arg_dict["whoami"]

if cmdline_arg_dict["verbose"]:
    base.set_loglevel(logging.DEBUG)
elif cmdline_arg_dict["terse"]:
    base.set_loglevel(logging.WARNING)
else:
    base.set_loglevel(logging.INFO)
my_logger = base.get_logger()
base.record_usage(sys.argv[0], whoami, cmdline_arg_dict)

error_message = ""
try:
    pattern = re.compile(reg_exp, re.IGNORECASE)
except sre_constants.error:
    error_message += "'{reg_exp}' is not a valid regular expression.".format(**locals())
if error_message:
    base.get_logger().critical(error_message)
    sys.exit(1)

data = cmdline_arg_dict["input-file"].readlines()

# Evaulate column headers
first_line = data.pop(0).rstrip(CR)
column_header_list = []
fields = first_line.split(delimiter_char)
if header_flag:
    if len(data) == 0:
        sys.exit()
    column_header_list = fields
else:
    if len(fields) == 0:
        sys.exit()
    # How many fields?
    zeroes = int(math.log10(len(fields)))
    column_header_list = ["Field" + str(x).rjust(1+zeroes, "0") for x in range(1, 1+len(fields))]
    # This data does not have a header line, so put back the line we extracted
    data.insert(0, first_line)

# Determine how to format output
length_longest_header_name = max([len(x) for x in column_header_list])
# How many records?
zeroes = int(math.log10(len(data)))

# Print data
for line_number, line in enumerate(data):
    if re.search(pattern, line):
        record_number = str(line_number+1).rjust(1+zeroes, "0")
        trailing_dashes = "-" * (80 - 11 - zeroes - 1)
        print("--[Record {record_number}]{trailing_dashes}".format(**locals()))
        field_list = line.rstrip(CR).split(delimiter_char)
        for i in range(len(column_header_list)):
            print("{0}: {1}".format(column_header_list[i].ljust(length_longest_header_name), field_list[i]))
