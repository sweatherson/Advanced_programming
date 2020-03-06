from Bio import Entrez
from Bio import SeqIO
import pprint
from Bio import Phylo
from urllib.error import HTTPError
from Bio.Align.Applications import MuscleCommandline
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor


Entrez.email = "b5025654@newcastle.ac.uk"


# class for a nested dictionary
class SingleDictionary(dict):

    def __init__(self):
        self.d = {}
    # add function which initialises the dictionary with a key name if a key name is not already present 
    def add(self, key, nestkey, value):
        if key not in self.d.keys():
            self.d[key] = {}           
        self.d[key][nestkey] = value
    #returns dictionary
    def get_d(self):
        return self.d
    #prints dictionary in readable format 
    def __str__(self):
        pprint.pprint(self.d)


# function to add dictionary to nested dictionary 
def add_to_dictionary(entry, search):
    gene_dict.add(entry, "Description", search.description) # description key and value
    gene_dict.add(entry, "Sequence", search.seq)            # sequence key and value
    return gene_dict.get_d()


"""search NCBI with accession number"""
def search():
    while True:
        entry = input("Please enter an accession number or enter \"quit\" to proceed: ")
        try:           
            if entry == "quit":   # if statement to suspend loop and proceed with other tasks
                break
            else:   # search in gb database for protein sequence record 
                handle = Entrez.efetch(db = "protein", id = entry, idtype = "acc", rettype = "gb", retmode = "text")
                record = SeqIO.read(handle, "genbank")
                result = add_to_dictionary(entry, record)    # add results to nested dictionary and store as variable 
        except HTTPError:
            print("An error has occured regarding the connection to the server. Please try again")
    return result 


# function to saerch for protein sequence within the dictionary and store data as fasta format within a file
def search_nest(d):
    with open("sequences.fasta", "w") as f:
        for id, info in d.items():
            for key in info:
                if key == "Sequence":
                    f.write("> "+ id + "\n" + str(info[key]+ "\n"))     # writes the results into a file in fasta format so that further manipulation can be achieved 
    return            


# function to perform multiple sequence aligment using muscle        
def multiple_alignment():
    muscle_exe = r"/home/steven/bin/muscle3.8.31_i86linux64"      # executable file 
    in_file = r"/home/steven/Database/sequences.fasta"            # input file containig fasta sequences 
    out_file = r"/home/steven/Database/alignment.fasta"           # output file where the alignment will be written to 
    muscle_cline = MuscleCommandline(muscle_exe, input= in_file, out = out_file)
    stdout, stderr = muscle_cline()                               # although variable not used, required to make sure file can be written to over and over
    MultiplSeqAligment = AlignIO.read(out_file, 'fasta')          # allow alignment file to be read
    print(MultiplSeqAligment)


# function for drawing phylogenetic tree
def draw_tree():
    calculator = DistanceCalculator('identity')                   # distance model used to calculate distances
    distance = calculator.get_distance(multi_align)               # calculate distance based on the model provided and input alignment file
    constructor = DistanceTreeConstructor()                       
    tree = constructor.upgma(distance)                            # construct tree based on UPGMA method
    Phylo.draw(tree)

# assign dictionary class to a variable 
gene_dict = SingleDictionary()

# assign results from search function to a variable
result_dict = search()

# search the given dictionary for the sequence data etc
search_nest(result_dict)

# print out readable dictionary ready for comparison against later results
gene_dict.__str__()

# perform multiple sequence alignment 
multiple_alignment()

# read the aligment file
multi_align = AlignIO.read('alignment.fasta', 'fasta')

# draw tree
draw_tree()



