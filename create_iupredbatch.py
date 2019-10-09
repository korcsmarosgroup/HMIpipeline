# specify host protein list for disordered region filtering
protein_list = 'host_protein_list.csv'
output_file = 'iupredbatch.sh'
# write command for performing disordered region filtering for every protein
with open(protein_list) as input_file:
    with open(output, 'w') as output_file:
        for line in input_file:
            protein = line.strip()
            output_file.write('./iupred ' + protein + '.fasta long >' + protein + '.txt' + "\n")