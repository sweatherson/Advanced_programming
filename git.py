from Bio import Entrez
from Bio import SeqIO
import collections
from collections import defaultdict
import pprint
from Bio import AlignIO
from Bio import Phylo

Entrez.email = "b5025654@newcastle.ac.uk"
    
class SingleDictionary(dict):

    def __init__(self):
        self.d = {}

    def add(self, key, nestkey, value):
        if (key not in self.d.keys()):
            self.d[key] = {}
        self.d[key][nestkey] = value
        if (key in self.d.keys()):
            raise DuplicateError ('Accession number: {s} already present'. format(key))
    def get_d(self):
        return self.d
        

class Error(Exception):
    """base class"""
    pass


class DuplicateError(Error):
    """accession number is a duplicate"""
    pass


gene_dict = SingleDictionary()

def add_to_dictionary(entry, search):
    gene_dict.add(entry, "Description", search.description)
    gene_dict.add(entry, "Sequence", search.seq)
    return gene_dict.get_d()


"""search NCBI with accession number"""
def search():
    while True:
        entry = input("Please enter an accession number: ")
        try:           
            if entry == "quit":
                break
            elif entry !=gene_dict.keys():
                handle = Entrez.efetch(db = "nucleotide", id = entry, idtype = "acc", rettype = "gb", retmode = "text")
                record = SeqIO.read(handle, "genbank")
                result = add_to_dictionary(entry, record)                              
    print(result)
    return result 


result_dict = search()


def search_nest(d):
    with open("sequences.fasta", "w") as f:
        for id, info in d.items():
            for key in info:
                if key == "Sequence":
                    f.write("> "+ id + "\n" + str(info[key]+ "\n"))     #writes the results into a file in fasta format so that further manipulation can be achieved 
    return            


search_nest(result_dict)
        

#align = AlignIO.read("sequence.fasta", clustal)


tree = Phylo.read ("sequences.fasta", "Newick")


hylo.draw_ascii(tree)


# AC004079.1 , AL121928.13