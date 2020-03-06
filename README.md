# **Advanced_programming CSC8311**
## Multiple sequence alignment analysis tool (proteins)
##### database.py contains main source code
A python application to search for proteins within the genbank database, store said proteins and perform a multiple sequence alignment once ready. The proteins are saerch for with their accession number and stored within a nested dictionary containing their description and sequence. Once all desired proteins have been entered, the application then writes each sequence to a file within the directory in a fasta format. This file is then aligned using MUSCLE and the output written to a seperate file within the directory. The final process produces a phylogenetic tree in a pdf using matplotlib and the phylo application within biopython. 



## Prerequisites 
### Software required

1. Biopython
```bash
python3.6 -m pip install biopython
```
2. Matplotlib
```bash
python3.6 -m pip install -U matplotlib
```
3. MUSCLE (Multiple Sequence Alignment tool)
```bash 
sudo apt install muscle
```
### Alterations required per user
In the ```multiple_alignment``` function (line 65), the files used are hard coded to my personal files. Therefore, these must be changed to appropriate file paths. 
## Example data
Example data used can be aquired here:
Accession number:
* P51494.1
* P05231.1
* P41323.1





 
