from pyfasta import Fasta
import re

def rename(fasta_key):
    fasta_key = fasta_key.split("|")
    fasta_key = fasta_key[1]
    return fasta_key

# fasta processing -> human.keys() print the keys, human[key_name] print the sequence
human = Fasta('humanproteins.fasta')

#elm identifier(key) - regex(value) dictionary
with open ("elm_motif.tsv", "r") as motif_table:
    motif_table.readline()
    elm_regex = {}
    for line in motif_table:
        line = line.strip().split("\t")
        elm_regex[line[1]] = line[4]

#motif(key) - domain(value list) dictionary
with open ("elm_interaction_domains.tsv", "r") as motif_domain_table:
    motif_domain_table.readline()
    motif_domain = {}
    for line in motif_domain_table:
        line = line.strip("\n").split("\t")
        if line[0] not in motif_domain:
            motif_domain[line[0]] = []
        motif_domain[line[0]].append(line[1])

#pfam(key) - uniprot(value list) dictionary
with open ("topprots_pfam.tab", "r") as legionella_domains_table:
    legionella_domains_table.readline()
    pfam_uniprot = {}
    for line in legionella_domains_table:
        line = line.strip().split("\t")
        if "," in line[1]:
            line[1] = line[1].split(",")
            for pfam in line[1]:
                if pfam not in pfam_uniprot:
                    pfam_uniprot[pfam] = []
                pfam_uniprot[pfam].append(line[0])

#uniprot(key) - motif(value list) dictionary
uniprot_motif = {}
for key in human.keys():
    for motif in elm_regex:
        match = re.search(str(elm_regex[motif]), str(human[key]))
        if match:
            if rename(key) not in uniprot_motif:
                uniprot_motif[rename(key)] = []
            #print("%s;%s;%s"%(motif,match.start(),match.end()))
            uniprot_motif[rename(key)].append((motif,str(match.start()),str(match.end())))
 

with open ("BtDMIresult_topprots.tsv", "w") as output:
    for pfam, uniprot_list in pfam_uniprot.items():
        for uniprot in uniprot_list:
            for motif in motif_domain:
                if pfam in motif_domain[motif]:
                    for uni, motif_list in uniprot_motif.items():
                        for motif_2 in motif_list:
                            if motif_2[0] == motif:
                                output.write(uni + ";" + ";".join(motif_2) + ";" + ";" + pfam+ ";" + uniprot + "\n")
