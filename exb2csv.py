import argparse
parser = argparse.ArgumentParser(description='Read annotations from .exb and extract statistics')
parser.add_argument('-x', '--input', required=True, help='The path of .txt file to process.')
parser.add_argument('-t', '--template', required=True, help='The path of template exb file')

args = parser.parse_args()

import os
import xml.dom.minidom as md
import csv

# first we read the full list of tiers from the template
fields = []

templ = md.parse(args.template)
for t in templ.getElementsByTagName('tier'):
    fields.append(t.getAttribute('display-name'))

print(fields)

file_exb = md.parse(args.input) 

rows = []

for t in file_exb.getElementsByTagName('tier'):

    # we will process the DOM based on the 'TXT' tier
    if t.getAttribute('display-name') == 'TXT':

        # scroll through all the words
        for w in t.getElementsByTagName('event'):
            txt = w.firstChild.data         # retrieve the word/text
            e_start = w.getAttribute('start')   # retreive event start
            e_end = w.getAttribute('end')       # retrieve event sto
            t_row = ['' for f in fields]    # init row elements
            t_row[0] = txt                  # init first elem as word

            for f in file_exb.getElementsByTagName('tier'): 
                # retrieve annotations (if any) for each field
                field_name = f.getAttribute('display-name')
                if (field_name != 'TXT'):
                    # retrieve the position of the field to know what column in the table it belongs to
                    pos = fields.index(field_name)  
                    # check if there's any annotation in this tier relative to the word we are processing
                    for a in f.getElementsByTagName('event'):
                        if (a.getAttribute('start') == e_start) and (a.getAttribute('end') == e_end):
                            # if start and end matches with the current word
                            # save the annotations in the relative column
                            t_row[pos] = a.firstChild.data
            # debug            
            print(t_row)
            # insert the row in the list of rows for csv file
            rows.append(t_row)

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


                    
                
            
