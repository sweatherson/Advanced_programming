from Bio import Entrez
from Bio import SeqIO
import pprint
from Bio import Phylo
from urllib.error import HTTPError
from Bio.Align.Applications import MuscleCommandline
import io
from Bio import AlignIO
Entrez.email = "b5025654@newcastle.ac.uk"


class SingleDictionary(dict):

    def __init__(self):
        self.d = {}

    def add(self, key, nestkey, value):
        if key not in self.d.keys():
            self.d[key] = {}           
        self.d[key][nestkey] = value

    def get_d(self):
        return self.d
        

class Error(Exception):
    """base class"""
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
            else:
                handle = Entrez.efetch(db = "protein", id = entry, idtype = "acc", rettype = "gb", retmode = "text")
                record = SeqIO.read(handle, "genbank")
                result = add_to_dictionary(entry, record)    
        except HTTPError:
            print("An error has occured regarding the connection to the server. Please try again")
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
        
muscle = MuscleCommandline(open("sequences.fasta"))
stout = muscle()
align = AlignIO.read(io.StringIO(stout), "fasta")
print(align)



#hylo.draw_ascii(tree)


# AC004079.1 , AL121928.13, 	AE006462.1

#AC073072.11, AC193002.3, AY083564.1, 
#P51494.1, P05231.1, P41323.1