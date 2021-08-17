import argparse
parser = argparse.ArgumentParser(description='Read annotations from .exb and create a .csv file')
parser.add_argument('-x', '--input', nargs='+', required=True, help='The path of .exb file to process. It is possible to process more than one file by specifying multiple paths or using a wildcard (*).')
parser.add_argument('-t', '--template', required=True, help='The path of template exb file')

args = parser.parse_args()

import os
import exb_utils
import csv

fields = exb_utils.read_fields(exb_template=args.template)
print(fields)


files_to_process = exb_utils.get_file_list(files_arg=args.input)

for f in files_to_process:

    rows = exb_utils.read_tokens_annotations(exb_input=f, fields=fields, debug=True)

    # create output file
    output_filename = os.path.basename(f).split('.')[0]
    output_filename = output_filename + '.csv'


    # writing to csv file
    with open(output_filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)

