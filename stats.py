with open('EN_op_1_57X32A15_31.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row[1])

