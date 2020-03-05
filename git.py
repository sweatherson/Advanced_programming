from Bio import Entrez
from Bio import SeqIO
import collections
from collections import defaultdict
import pprint
from Bio import AlignIO
from Bio import Phylo

Entrez.email = "b5025654@newcastle.ac.uk"
    
class single_dictionary(dict):
    def __init__(self):
        self = defaultdict()
    def add(self, key, value):
        self[key] = value
        return self



class Error(Exception):
    """base class"""
    pass


class DuplicateError(Error):
    """accession number is a duplicate"""
    pass


gene_dict = single_dictionary()

def add_too_dictionary(search):
    gene_dict.add("Description", search.description)
    gene_dict.add("Sequence", search.seq)
    return gene_dict


nested_dict ={}


def add_to_nested(entry, search):
    nested_dict[entry] = add_too_dictionary(search)
    return nested_dict

def add_to_nested_update(entry, search):
    nested_dict[entry].update({add_too_dictionary(search)})
    return nested_dict

"""search NCBI with accession number"""
def search():
    while True:
        n = 0
        try:
            entry = input("Please enter an accession number: ")
            if entry == "q":
                break
            elif entry !=gene_dict.keys() and n < 1:
                handle = Entrez.efetch(db = "nucleotide", id = entry, idtype = "acc", rettype = "gb", retmode = "text")
                record = SeqIO.read(handle, "genbank")
                add_to_nested (entry, record)                
                pprint.pprint(nested_dict)
                n = n + 1
            elif entry != gene_dict.keys():
                handle = Entrez.efetch(db = "nucleotide", id = entry, idtype = "acc", rettype = "gb", retmode = "text")
                record = SeqIO.read(handle, "genbank")
                add_to_nested_update(entry, record)
            elif entry == gene_dict.keys():
                raise DuplicateError               
        except DuplicateError:
            print ("Accession Number already entered! Please enter a new Accession Number")

    return 



search()


def search_nest(d):
    for id, info in d.items():
        for key in info:
            if key == "Sequence":
                f = open( "sequences.fasta", "w")
                f.write("> "+ id + "\n" + str(info[key]))     #writes the results into a file in fasta format so that further manipulation can be achieved 
                f.close()
                return


search_nest(nested_dict)
        

align = AlignIO.read("sequence.fasta", clustal)


tree = Phylo.read ("sequence.fasta", "Newick")


Phylo.draw_ascii(tree)


# AC004079.1 , AL121928.13