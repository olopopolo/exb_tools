import argparse
parser = argparse.ArgumentParser(description='Read annotations from x2 .exb files and extract statistics')
parser.add_argument('-x', '--input1', required=True, help='The path of .exb file to process.')
parser.add_argument('-y', '--input2', required=True, help='The path of .exb file to process.')

args = parser.parse_args()

import exb_utils
import sys

fields1 = exb_utils.read_fields(exb_template=args.input1)
fields2 = exb_utils.read_fields(exb_template=args.input2)

if not (fields1 == fields2):  # check that we have the exact same tiers in the two files
    print('WARNING! The two files do NOT have the same tiers/fields!')
    sys.exit(1)

# read rows from both files
rows1, tokens1 = exb_utils.read_tokens_annotations(exb_input=args.input1, fields=fields1, debug=False)
rows2, tokens2 = exb_utils.read_tokens_annotations(exb_input=args.input2, fields=fields2, debug=False)

if not (tokens1 == tokens2):  # check that we have the exact same tiers in the two files
    print('WARNING! The two files have tokens not matching with each other!!')
    sys.exit(1)

def avg(list):
    return sum(list)/len(list)

CKappa_score = []

# let's compute Cohen's Kappa statistics for each tier
for ix_f, f in enumerate(fields1):
    if ix_f == 0:
        continue    # skip the first column, i.e. the token column

    field_scores = []
    for ix_t, t in enumerate(rows1):    # for each row/token
        annotation_list1 = exb_utils.get_column(rows1, ix_f)    # retrieve annotations for the tier/column to be analyzed
        annotation_list2 = exb_utils.get_column(rows2, ix_f)

        score = exb_utils.cohen_kappa(annotation_list1, annotation_list2)

        if not score is None:
            field_scores.append(
                score
            )

    if len(field_scores) > 0:
        CKappa_score.append(
            avg(field_scores)
        )    # append average score for this field
        print(f, 'average score:', avg(field_scores))
    else:
        print('WARNING: Ignoring field', f)

print()
print('AVERAGE Inter Annotator Agreement for all tiers (excluding ignored/single class fields):')
print(avg(CKappa_score))






