import argparse
parser = argparse.ArgumentParser(description='Create .exb file from .txt')
parser.add_argument('-t', '--template', required=True, help='The path of template exb file')
parser.add_argument('-x', '--input', required=True, help='The path of .txt file to process.')

args = parser.parse_args()

import os
import xml.dom.minidom as md

txt_filename = args.input
txt_data = open(txt_filename,'r')
# read the txt file
my_string = txt_data.read()
word_list = my_string.split(' ')
# parse the xml/exb template file
file = md.parse(args.template)
# create the tli objects for each word into common-timeline
for i,w in enumerate(word_list):
    tli = file.createElement( "tli" )
    tli.setAttribute('id','T'+str(i))
    file.getElementsByTagName('common-timeline')[0].appendChild(tli)
# create the event objects for each word into the first tier
for i,w in enumerate(word_list):
    event = file.createElement( "event" )
    event.setAttribute('end','T'+str(i+1))
    event.setAttribute('start','T'+str(i))
    value = file.createTextNode(w)
    event.appendChild(value)
    file.getElementsByTagName('tier')[0].appendChild(event)
# create output file
output_filename = os.path.basename(args.input).split('.')[0]
output_filename = output_filename + '.exb'
with open(output_filename, "w" ) as fs:
    fs.write( file.toxml() )
    fs.close()

