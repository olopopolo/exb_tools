import argparse
parser = argparse.ArgumentParser(description='Read annotations from x2 .exb files and extract statistics')
parser.add_argument('-x', '--input1', required=True, help='The path of .exb file to process.')
parser.add_argument('-y', '--input2', required=True, help='The path of .exb file to process.')
parser.add_argument('--thresh', type=float, default=1.0, help='Kappa score threshold. When the Kappa is below this value, a confusion matrix is generated.')
parser.add_argument('--outdir', default=None, help='Choose where to store the output data (plots and other things). If not specified, the first file\'s path (specified with -x/--input1) will be used.')

args = parser.parse_args()

import exb_utils
import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn
import sklearn.metrics
import os

fields1 = exb_utils.read_fields(exb_template=args.input1)
fields2 = exb_utils.read_fields(exb_template=args.input2)

if not (fields1 == fields2):  # check that we have the exact same tiers in the two files
    print('ERROR! The two files do NOT have the same tiers/fields!')
    sys.exit(1)

# read rows from both files
rows1, tokens1 = exb_utils.read_tokens_annotations(exb_input=args.input1, fields=fields1, debug=False)
rows2, tokens2 = exb_utils.read_tokens_annotations(exb_input=args.input2, fields=fields2, debug=False)

if not (tokens1 == tokens2):  # check that we have the exact same tiers in the two files
    print('ERROR! The two files have tokens not matching with each other!!')
    sys.exit(1)

def avg(list):
    return sum(list)/len(list)

CKappa_score = []
CKappa_score_labels = []

# let's compute Cohen's Kappa statistics for each tier
for ix_f, f in enumerate(fields1):
    if ix_f == 0:
        continue    # skip the first column, i.e. the token column

    field_scores = []
    field_scores_labels = []

    annotation_list1 = exb_utils.get_column(rows1, ix_f)    # retrieve annotations for the tier/column to be analyzed
    annotation_list2 = exb_utils.get_column(rows2, ix_f)

    score = exb_utils.cohen_kappa(annotation_list1, annotation_list2)

    if not score is None:
        field_scores.append(score)

        if not (f in ['Verb_Target Hypothesis0', 'Verb_ Target Hypothesis 1']): # skip the first two tiers, as they don't have any label associated
            kappa = sklearn.metrics.cohen_kappa_score(annotation_list1, annotation_list2, labels=exb_utils.labels_map[f])
            if kappa < args.thresh:
                cm = sklearn.metrics.confusion_matrix(annotation_list1, annotation_list2, labels=exb_utils.labels_map[f]) # what to do with this?
                print('Tier:', f)
                #print('Labels: ', exb_utils.labels_map[f])
                #print(cm)
                sanitized_labels = [l if l != '' else 'empty' for l in exb_utils.labels_map[f]]
                df_cm = pd.DataFrame(cm, sanitized_labels, sanitized_labels)
                sn.set(font_scale=0.7)
                sn.heatmap(df_cm, annot=True)  # font size
                plt.title('Tier: '+f)
                plt.xlabel('Annotator 2')
                plt.ylabel('Annotator 1')

                # save the plot and other info in a dedicated folder
                folder_name = os.path.basename(args.input1)
                folder_name = os.path.splitext(folder_name)[0]  # strip the extension
                if args.outdir is None:
                    dirpath = os.path.dirname(args.input1)  # if no name is specified, args.input1 path is used
                else:
                    dirpath = args.input1

                dirpath = os.path.join(dirpath, folder_name)    # create the folder for output files in the desired one

                if not os.path.isdir(dirpath):      # check if dir exists
                    os.makedirs(dirpath)

                filename = f

                plt.savefig(os.path.join(dirpath, filename))
                plt.clf()   # clear the figure for next iterations

                # let's also report what labels are different for each token
                differences = [[i, annotation_list1[i], annotation_list2[i]] for i in range(len(annotation_list1)) if annotation_list1[i] != annotation_list2[i]]

                with open(os.path.join(dirpath,filename+'_diff.txt'), 'w') as filediff:
                    filediff.write('POS\tANN1\tANN2\n')
                    for d in differences:
                        if d[1] == '':
                            d[1] = 'empty'
                        if d[2] == '':
                            d[2] = 'empty'
                        line = str(d[0])+'\t'+d[1]+'\t'+d[2]
                        line += '\n'
                        filediff.write(line)

        else:
            kappa = sklearn.metrics.cohen_kappa_score(annotation_list1, annotation_list2)

        field_scores_labels.append(kappa)




    if len(field_scores) > 0:
        CKappa_score.append(avg(field_scores))    # append average score for this field
        CKappa_score_labels.append(avg(field_scores_labels))
        print(f, 'average score:\t', "{:.4f}".format(avg(field_scores)), 'no labels,\t', "{:.4f}".format(avg(field_scores_labels)), 'considering labels')
    else:
        print('WARNING: Ignoring field', f)

print()
print('AVERAGE Inter Annotator Agreement for all tiers (excluding ignored/single class fields):')
print(avg(CKappa_score))
print('AVERAGE Inter Annotator Agreement for all tiers CONSIDERING LABELS (excluding ignored/single class fields):')
print(avg(CKappa_score_labels))





