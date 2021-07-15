import xml.dom.minidom as md



def read_fields(exb_template):
    """
    Read all the fields from a template file
    :param exb_template: the .exb template file to inspect
    :return: a list of fields
    """
    fields = []

    templ = md.parse(exb_template)
    for t in templ.getElementsByTagName('tier'):
        fields.append(t.getAttribute('display-name'))

    return fields


def read_tokens_annotations(exb_input, fields, debug=False):


    file_exb = md.parse(exb_input)

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
                if debug:
                    print(t_row)

                # insert the row in the list of rows for csv file
                rows.append(t_row)

    return rows, get_column(rows, 0)

def get_column(rows, column_idx):
    return [r[column_idx] for r in rows]


def cohen_kappa(ann1: list, ann2: list, verbose=False):
    """Computes Cohen kappa for pair-wise annotators.
    :param ann1: annotations provided by first annotator
    :type ann1: list
    :param ann2: annotations provided by second annotator
    :type ann2: list
    :rtype: float
    :return: Cohen kappa statistic
    """
    count = 0
    for an1, an2 in zip(ann1, ann2):
        if an1 == an2:
            count += 1
    A = count / len(ann1)  # observed agreement A (Po)

    uniq = set(ann1 + ann2)
    E = 0  # expected agreement E (Pe)
    for item in uniq:
        cnt1 = ann1.count(item)
        cnt2 = ann2.count(item)
        count = ((cnt1 / len(ann1)) * (cnt2 / len(ann2)))
        E += count

    if E == 1.0:
        if verbose:
            print('WARNING Cohen\'s Kappa: single class agreement. E == 1.0, this would incur in a float division by 0.')
        return None
    else:
        return round((A - E) / (1 - E), 4)