# Tools to process .exb files
## Convert .txt to .exb files
The script `txt2exb.py` is used to read a text file and insert into a template ready to be annotated by linguistics experts. The command works as follow:
```
py txt2exb.py -x <txt file path> -t <template file path>
```
## Convert .exb to .csv files
The script `exb2csv.py` is used to read a exb annotated file and convert it into a csv file format, ready to be read into data processing pipelines. The command works as follow. Note that the template file must be the same used during the .txt to .exb conversion.
```
py exb2csv.py -x <annotated exb file path> -t <template file path>
```
