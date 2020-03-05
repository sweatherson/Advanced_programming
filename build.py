from Bio import Entrez
from Bio import SeqIO
import collections
from collections import defaultdict

Entrez.email = "b5025654@newcastle.ac.uk"

    
class single_dictionary(dict):
    def __init__(self):
        self = dict()
    def add(self, key, value):
        self[key] = value



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
    return


"""search NCBI with accession number"""
def search():
    while True:
        try:
            entry = input("Please enter an accession number: ")
            if entry == "q":
                break
            elif entry !=gene_dict.keys():
                handle = Entrez.efetch(db = "nucleotide", id = entry, idtype = "acc", rettype = "gb", retmode = "text")
                record = SeqIO.read(handle, "genbank")
                add_to_nested (entry, record)
                print(nested_dict)
            elif entry == gene_dict.keys():
                raise DuplicateError               
        except DuplicateError:
            print ("Accession Number already entered! Please enter a new Accession Number")

    return 



search()


## going wrong in the add_to_nested function. 



        



# AC004079.1 , AL121928.13

# ['__add__', '__bool__', '__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__le___', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__radd__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_per_letter_annotations', '_seq', '_set_per_letter_annotations', '_set_seq', 'annotations', 'dbxrefs', 'description', 'features', 'format', 'id', 'letter_annotations', 'lower', 'name', 'reverse_complement', 'seq', 'translate', 'upper']