import argparse
import os


def ddi(bacterial_input, bacterial_id_col, bacterial_pf_col, human_input,
        human_id_col, human_pf_col, output_file_path, output_file_info_path):
    bacterial_id_col = bacterial_id_col - 1
    bacterial_pf_col = bacterial_pf_col - 1

    human_id_col = human_id_col - 1
    human_pf_col = human_pf_col - 1

    # make a set from database iteractions
    DDI = set()
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'resources/pfam_iteractions.txt')) as ddi_file:
        for line in ddi_file:
            line = line.strip()
            cell = line.split()

            # add ddi to set like: pfam1;pfam2 and pfam2;pfam1 because undirected
            DDI.add(f"{cell[0]};{cell[1]}")
            DDI.add(f"{cell[1]};{cell[0]}")

    bac_file = []
    with open(bacterial_input) as bacterial_input_file:
        for line in bacterial_input_file:
            bac_file.append(line.strip().split())

    human_file = []
    with open(human_input) as human_input_file:
        for line in human_input_file:
            human_file.append(line.strip().split())

    predictions = 0

    with open(output_file_info_path, 'w') as outfile_info:
        with open(output_file_path, 'w') as outfile:
            for cells1 in bac_file:
                for cells2 in human_file:
                    bacpfam = cells1[bacterial_pf_col]
                    #print(bacpfam)
                    humanpfam = cells2[human_pf_col]
                    #print(humanpfam)
                    ddi_test = f"{bacpfam};{humanpfam}"
                    #print(ddi_test)
                    if ddi_test in DDI:
                        predictions += 1
                        #print(f"Found combination: {cells1} == {cells2}")
                        outfile_info.write("\t".join(cells1) + "\t" +
                                           "\t".join(cells2) + "\n")
                        outfile.write(
                            f"{cells1[bacterial_id_col]}\t{cells2[human_id_col]}\n"
                        )
    return predictions


def main():
    parser = argparse.ArgumentParser(description="DDI Based PPI Prediction")
    parser.add_argument('--bacterial_input', type=str)
    parser.add_argument('--bacterial_id_col', type=int)
    parser.add_argument('--bacterial_pf_col', type=int)
    parser.add_argument('--human_input', type=str)
    parser.add_argument('--human_id_col', type=int)
    parser.add_argument('--human_pf_col', type=int)
    parser.add_argument('--output_file_path', type=str, default='DDIpreds.txt')
    parser.add_argument('--output_file_info_path',
                        type=str,
                        default='DDIpreds_with_info.txt')

    args = vars(parser.parse_args())

    predictions = ddi(**args)

    print(
        f"--- DDI FINISHED!\n- # PREDICTIONS: {predictions}\n- Output file: {args['output_file_path']} and {args['output_file_info_path']}"
    )


if __name__ == "__main__":
    main()

#cells1 = ['CLST014322', 'DNA-directed_RNA_polymerase,_beta_subunit/140_kD_subunit', 'unknown', 'Healthycore', 'PF04561.7', 'PF04561']
#cells2 = ['U3KPV4', 'PF03414']