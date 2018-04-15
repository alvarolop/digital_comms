# -*- coding: utf-8 -*-
import os
import csv
import pprint

###############
# Variables

FILE_FOLDER = "D:\Dropbox\\00TFM\Digital Comms Input" # This is an example
#FILE_FOLDER = "/home/tom/Dropbox/Digital Comms - Cambridge data" # Another example
INPUT_FILENAME = "complete_file.csv"
OUTPUT_FILENAME = "file_uk.csv"

###############
# Read the .csv file and store the content in an array
content = []

input_file = os.path.join(FILE_FOLDER, INPUT_FILENAME)
print (input_file)
with open(input_file, 'r') as my_file:
    reader = csv.reader(my_file)
    next(reader)  # skip header
    for header1, header2 in reader: # <= Modify header1, header2, etc. with the correct name.
        if (header1 == "UK"): #Filter elements from UK
            content.append({
                "header1": header1, # <= Modify header1, header2, etc. with the correct name.
                "header2": header2  # <= Modify header1, header2, etc. with the correct name.
            })
    
    
# Print values of content:
pprint.pprint (repr(list(content)))


# Create a new .csv file with the filtered elements
output_filename = os.path.join(FILE_FOLDER, OUTPUT_FILENAME)
output_file = open(output_filename, 'w', newline='')
writer = csv.writer(output_file)
writer.writerow(('header1', 'header2')) # <= Modify header1, header2, etc. with the correct name.

for row in content:
    writer.writerow(row.header1, row.header2) # <= Modify header1, header2, etc. with the correct name.
output_file.close()