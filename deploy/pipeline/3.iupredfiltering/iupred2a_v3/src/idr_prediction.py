import argparse
import os
import sys
import urllib.request as urllib
from iupred2a import read_seq, iupred, anchor2

import random
import time


def parse_args(argv):
    """ Command line interface for the the module """
    parser = argparse.ArgumentParser()
    parser.add_argument("--hmi_prediction",
                        help="<path to an existing FILE> [mandatory]",
                        dest="hmi_prediction",
                        action="store",
                        required=True)

    parser.add_argument("--resources",
                        help="<path to resources FILES> [mandatory]",
                        dest="resources",
                        action="store",
                        required=True)

    parser.add_argument("--results",
                        help="<path to results> [mandatory]",
                        dest="results",
                        action="store",
                        required=True)

    results = parser.parse_args(argv)
    return results


def process_hmi(file):
    """ Opening hmi file and select the human interactors """
    with open(file) as hmi_table:
        human_proteins = []
        for line in hmi_table:
            line = line.strip().split(";")
            protein = line[0]
            if protein not in human_proteins:
                human_proteins.append(protein)
    print(len(human_proteins))
    return human_proteins


def get_interaction(file):
    """ Opening hmi file and select the human interactors """
    with open(file) as hmi_table:
        hmi = []
        for line in hmi_table:
            line = line.strip().split(";")
            hmi.append(line)
    print(len(hmi))
    return hmi


def get_motif(file):
    """ Get information about bacteria interacting human motifs """
    with open(file) as hmi_table:
        motif = {}
        for line in hmi_table:
            line = line.strip().split(";")
            if line[0] not in motif:
                motif[line[0]] = set()
            motif[line[0]].add((line[1], line[2], line[3]))

    return motif


def download_fasta(protein_list, folder):
    """ Downloading fasta sequences from Uniprot """
    sequence_folder = "{}/protein_sequences".format(folder)
    for protein in protein_list:
        if protein.endswith('.DS_Store'):
            continue
        url = 'http://www.uniprot.org/uniprot/' + protein + '.fasta'
        wait = random.uniform(0.1, 1.0)
        result = urllib.urlopen(url)
        result = result.read()
        result = result.decode().split("\n")
        time.sleep(wait)
        output_name = os.path.join(sequence_folder, protein + '.fasta')
        with open(output_name, 'w') as output_file:
            output_file.write("\n".join(result))


def run_iupred(folder, method_type='short', anchor=True):
    """ IUPred modelling with an optional usage of ANCHOR2 """
    motif_score = {}
    sequence_folder = "{}/protein_sequences".format(folder)
    iupred_data_folder = "{}/iupred_data".format(folder)
    for sequence in os.listdir(sequence_folder):
        protein_name = str(sequence).split(".")[0]
        sequence = read_seq(os.path.join(sequence_folder, sequence))
        iupred2_result = iupred(iupred_data_folder, sequence, method_type)
        if anchor:
            if method_type == 'long':
                anchor2_res = anchor2(iupred_data_folder, sequence, iupred2_result[0])
            else:
                anchor2_res = anchor2(iupred_data_folder, sequence, iupred(iupred_data_folder, sequence, 'long')[0])
        if method_type == 'glob':
            motif_score[protein_name] = iupred2_result[1]
        for pos, residue in enumerate(sequence):
            output_list = [protein_name, str(pos + 1), residue, str(iupred2_result[0][pos])]
            if anchor:
                output_list = [protein_name, str(pos + 1), residue, str(iupred2_result[0][pos]), str(anchor2_res[pos])]
            if protein_name not in motif_score:
                motif_score[protein_name] = []
            motif_score[protein_name].append(output_list[1:])


    return motif_score


def motif_selection(aa_scores, motif_dictionary):
    """ Selection of disordered motifs """
    disordered_motifs = []
    print(len(aa_scores))
    for protein in aa_scores:
        print(protein)
        if protein in motif_dictionary:
            print(protein)
            for list_ in motif_dictionary[protein]:
                motif = range(int(list_[1]), int(list_[2])+1)
                motif_size = len(motif)
                dis_aa_count = 0
                for details in aa_scores[protein]:
                    if int(details[0]) in motif:
                        if (float(details[2]) > 0.5) and (float(details[3]) > 0.4):
                            dis_aa_count += 1
                if (dis_aa_count == motif_size) or (dis_aa_count == motif_size - 1) or (dis_aa_count == motif_size + 1):
                    disordered_motifs.append((protein, list_[0], list_[1], list_[2]))
    return disordered_motifs


def write_output(folder, idr_motifs, hmi, anchor=True):
    """ Writing output file """
    output_file = folder + "/idr_motifs.csv"
    with open(output_file, 'w') as output_file:
        output_file.write("# Human Protein" + "\t" + "Motif" + "\t" +  "Start" + "\t" +  "End" +
                          "\t" +"Bacterial domain" + "\t" + "Bacterial protein" "\n")

        idr_motifs = list(set(idr_motifs))

        for motif in idr_motifs:
            for interaction in hmi:
                if motif[0] in interaction and motif[1] in interaction:
                    output_file.write("\t".join(interaction) + "\n")


def main(argv):
    """ Main method and logic """

    # Read args
    args = parse_args(argv)

    # Get human interactors from the HMI prediction
    human_proteins = process_hmi(args.hmi_prediction)
    hmi = get_interaction(args.hmi_prediction)

    # Get interacting motif information
    motif_dict = get_motif(args.hmi_prediction)

    # Download fasta files - 1 protein/file
    download_fasta(human_proteins, args.resources)

    # Assign IUPred and ANCHOR scores to AAs
    scores = run_iupred(args.resources, 'short')

    # Select disordered motifs
    idr_motifs = motif_selection(scores, motif_dict)

    # Write the output file
    write_output(args.results, idr_motifs, hmi)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))