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


class SingleDictionary(dict):

    def __init__(self):
        self.d = {}

    def add(self, key, nestkey, value):
        if key not in self.d.keys():
            self.d[key] = {}           
        self.d[key][nestkey] = value

    def get_d(self):
        return self.d
    def __str__(self):
        pprint.pprint(self.d)




gene_dict = SingleDictionary()


def add_to_dictionary(entry, search):
    gene_dict.add(entry, "Description", search.description)
    gene_dict.add(entry, "Sequence", search.seq)
    return gene_dict.get_d()


"""search NCBI with accession number"""
def search():
    while True:
        entry = input("Please enter an accession number or enter \"quit\" to proceed: ")
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
        
def multiple_alignment():
    muscle_exe = r"/home/steven/bin/muscle3.8.31_i86linux64"
    in_file = r"/home/steven/Database/sequences.fasta"
    out_file = r"/home/steven/Database/alignment.fasta"
    muscle_cline = MuscleCommandline(muscle_exe, input= in_file, out = out_file)
    stdout, stderr = muscle_cline()
    MultiplSeqAligment = AlignIO.read(out_file, 'fasta')
    print(MultiplSeqAligment)

multiple_alignment()

multi_align = AlignIO.read('alignment.fasta', 'fasta')

def draw_tree():
    calculator = DistanceCalculator('identity')
    distance = calculator.get_distance(multi_align)
    constructor = DistanceTreeConstructor()
    tree = constructor.upgma(distance)
    Phylo.draw(tree)


draw_tree()



#hylo.draw_ascii(tree)


# AC004079.1 , AL121928.13, 	AE006462.1

#AC073072.11, AC193002.3, AY083564.1, 
#P51494.1, P05231.1, P41323.1