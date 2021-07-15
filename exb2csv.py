import argparse
parser = argparse.ArgumentParser(description='Read annotations from .exb and create a .csv file')
parser.add_argument('-x', '--input', required=True, help='The path of .exb file to process.')
parser.add_argument('-t', '--template', required=True, help='The path of template exb file')

args = parser.parse_args()

import os
import exb_utils

fields = exb_utils.read_fields(exb_template=args.template)

print(fields)

rows = exb_utils.read_tokens_annotations(exb_input=args.input, fields=fields, debug=True)

import csv

# create output file
output_filename = os.path.basename(args.input).split('.')[0]
output_filename = output_filename + '.csv'


# writing to csv file 
with open(output_filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(rows)

