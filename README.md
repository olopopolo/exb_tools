# Tools to process .exb files
## Convert .txt to .exb files
The script `txt2exb.py` is used to read a text file and insert into a template ready to be annotated by linguistics experts. The command works as follow:
```
py txt2exb.py -x <txt file path> -t <template file path>
```
Note that now it's possible to input multiple files and use a wildcard (i.e. `*`) to select multiple files to be processed. See the following example:
```shell script
# specify each file sequentially as a list
py txt2exb.py -x file1.txt file2.txt file3.txt -t <template file path>

# specify files using a wildcard 
# in this case, all files that matches the pattern `file*.txt` 
# (i.e. file1.txt, file99.txt file99_y.txt, etc.) 
py txt2exb.py -x file*.txt -t <template file path>
```

## Convert .exb to .csv files
The script `exb2csv.py` is used to read a exb annotated file and convert it into a csv file format, ready to be read into data processing pipelines. The command works as follow. Note that the template file must be the same used during the .txt to .exb conversion.
```
py exb2csv.py -x <annotated exb file path> -t <template file path>
```
Similarly, is it possible to input multiple files and use a wildcard (i.e. `*`) to select multiple files to be processed.

## Compute Inter Annotator Agreement
The script `exb2IAA.py` is used to compute IAA between two .exb files.
```
usage: exb2IAA.py [-h] -x INPUT1 -y INPUT2 [--thresh THRESH] [--outdir OUTDIR]

Read annotations from x2 .exb files and extract statistics

optional arguments:
  -h, --help            show this help message and exit
  -x INPUT1, --input1 INPUT1
                        The path of .exb file to process.
  -y INPUT2, --input2 INPUT2
                        The path of .exb file to process.
  --thresh THRESH       Kappa score threshold. When the Kappa is below this
                        value, a confusion matrix is generated.
  --outdir OUTDIR       Choose where to store the output data (plots and other
                        things). If not specified, the first file's path
                        (specified with -x/--input1) will be used.
```
