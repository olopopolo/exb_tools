import argparse
parser = argparse.ArgumentParser(description='Read annotations from x2 .exb files and extract statistics')
parser.add_argument('-x', '--input1', required=True, help='The path of .exb file to process.')
parser.add_argument('-y', '--input2', required=True, help='The path of .exb file to process.')
parser.add_argument('--thresh', type=float, default=1.0, help='Kappa score threshold. When the Kappa is below this value, a confusion matrix is generated.')

args = parser.parse_args()

import exb_utils
import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn
import sklearn.metrics

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

    for ix_t, t in enumerate(rows1):    # for each row/token
        annotation_list1 = exb_utils.get_column(rows1, ix_f)    # retrieve annotations for the tier/column to be analyzed
        annotation_list2 = exb_utils.get_column(rows2, ix_f)

        score = exb_utils.cohen_kappa(annotation_list1, annotation_list2)

        if not score is None:
            field_scores.append(score)

            if not (f in ['Verb_Target Hypothesis0', 'Verb_ Target Hypothesis 1']): # skip the first two tiers, as they don't have any label associated
                kappa = sklearn.metrics.cohen_kappa_score(annotation_list1, annotation_list2, labels=exb_utils.labels_map[f])
                if kappa < args.thresh:
                    cm = sklearn.metrics.confusion_matrix(annotation_list1, annotation_list2, labels=exb_utils.labels_map[f]) # what to do with this?
                    print('Tier:', f, '- Token:', t)
                    print('Labels: ', exb_utils.labels_map[f])
                    print(cm)
                    df_cm = pd.DataFrame(cm, exb_utils.labels_map[f], exb_utils.labels_map[f])
                    #sn.set(font_scale=1.4)
                    sn.heatmap(df_cm, annot=True)  # font size
                    plt.title(args.input1+' - '+f)
                    plt.xlabel('Annotator 2')
                    plt.ylabel('Annotator 1')
                    plt.show()
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





