# specify bacterial protein list
protein_list = 'bacterial_protein_list.csv'
# collect commands for downloading sequences corresponding to every protein
output_file = 'fastdownload.sh'

with open(protein_list) as input_file:
    with open(output, 'w') as output_file:
        for line in input_file:
            protein = line.strip()
            output_file.write('wget http://www.uniprot.org/uniprot/' + protein + '.fasta' + "\n")
