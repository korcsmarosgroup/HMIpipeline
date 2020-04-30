import argparse
import re

from pyfasta import Fasta


def dmi(bacterial_input, bacterial_id_col, bacterial_pf_col, human_receptors_DMI,
        output_file_path):
    bacterial_id_col = bacterial_id_col - 1
    bacterial_pf_col = bacterial_pf_col - 1

    # def rename(fasta_key):
    #     fasta_key = fasta_key.split("|")
    #     fasta_key = fasta_key[0]
    #     return fasta_key

    # fasta processing -> human.keys() print the keys, human[key_name] print the sequence
    human = Fasta(human_receptors_DMI)  #'human_receptors.fasta')

    #elm identifier(key) - regex(value) dictionary
    with open("elm_motif.tsv", "r") as motif_table:
        motif_table.readline()
        elm_regex = {}
        for line in motif_table:
            line = line.strip().split("\t")
            elm_regex[line[1]] = line[4]

    #motif(key) - domain(value list) dictionary
    with open("elm_interaction_domains.tsv", "r") as motif_domain_table:
        motif_domain_table.readline()
        motif_domain = {}
        for line in motif_domain_table:
            line = line.strip("\n").split("\t")
            if line[0] not in motif_domain:
                motif_domain[line[0]] = []
            motif_domain[line[0]].append(line[1])

    #pfam(key) - uniprot(value list) dictionary
    with open(bacterial_input, "r") as bacterial_proteins:
        bacterial_proteins.readline()
        bacterial_proteins = [a.strip().split("\t") for a in bacterial_proteins]
        pfam_uniprot = dict([
            (a[bacterial_pf_col], []) for a in bacterial_proteins
        ])
        for line in bacterial_proteins:
            pfam_uniprot[line[bacterial_pf_col]].append(line[bacterial_id_col])

    #uniprot(key) - motif(value list) dictionary
    uniprot_motif = {}
    for key in human.keys():
        for motif in elm_regex:
            match = re.search(str(elm_regex[motif]), str(human[key]))
            if match:
                if key not in uniprot_motif:
                    uniprot_motif[key] = []
                #print("%s;%s;%s"%(motif,match.start(),match.end()))
                uniprot_motif[key].append(
                    (motif, str(match.start()), str(match.end())))

    with open(output_file_path, "w") as output:
        predictions = 0
        for pfam, uniprot_list in pfam_uniprot.items():
            for uniprot in uniprot_list:
                for motif in motif_domain:
                    if pfam in motif_domain[motif]:
                        for uni, motif_list in uniprot_motif.items():
                            for motif_2 in motif_list:
                                if motif_2[0] == motif:
                                    predictions += 1
                                    output.write(uni + ";" + ";".join(motif_2) +
                                                 ";" + ";" + pfam + ";" +
                                                 uniprot + "\n")
    return predictions


def main():
    parser = argparse.ArgumentParser(description="DMI")
    parser.add_argument('--bacterial_input', type=str)
    parser.add_argument('--bacterial_id_col', type=int)
    parser.add_argument('--bacterial_pf_col', type=int)
    parser.add_argument('--human_receptors_DMI', type=str)
    parser.add_argument('--output_file_path',
                        type=str,
                        default='MPDMIresult.tsv')

    args = vars(parser.parse_args())

    predictions = dmi(**args)

    print(
        f"--- DMI FINISHED!\n- # PREDICTIONS: {predictions}\n- Output file: {args['output_file_path']}"
    )


if __name__ == "__main__":
    main()
