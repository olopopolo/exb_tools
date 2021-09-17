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
py exb2IAA.py -x <annotator-1 .exb file path> -y <annotator-2 .exb file path>
```
