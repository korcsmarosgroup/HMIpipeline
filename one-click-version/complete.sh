#!/bin/bash

###########################################################################
###########################################################################
#### MicrobioLink pipeline
###########################################################################

#sh pipeline_execution.sh "Metaproteome.txt" 1 2 "humanDDI.txt" 1 2 "humanDMI.fasta" "Tie_Die_downstream.input" ALL uniprot


### PASTE ABOVE THE NAME OF YOUR INPUTS:

bacterial_proteins=$1
#"Metaproteome.txt"
bacterial_id_col=$2
#1
bacterial_pf_col=$3
#2

human_receptors_DDI=$4
#"humanDDI.txt"
human_id_col=$5
#1
human_pf_col=$6
#2

human_receptors_DMI=$7
#"humanDMI.fasta"

target_genes_file=$8
#"Tie_Die_downstream.input"

DDInDMI=$9
#"ALL" or "DDI" or "DMI"

id_format=$10
#"genename" or "uniprot"

###
main_dir="$(pwd)"
pipe_dir="$main_dir/deploy/pipeline"



########################################################
### STEP 1: INTERACTION PREDICTION

############################
# Domain-domain interaction

cd user_inputs

if [ $DDInDMI = "DDI" ] || [ $DDInDMI = "ALL" ]; then
	
cp $bacterial_proteins $pipe_dir/1.DDI/Metaproteome_pfam_forDDI.txt
cp $human_receptors_DDI $pipe_dir/1.DDI/humanprots_pfam_forDDI.txt

cd $pipe_dir/1.DDI/
echo "----STARTING DDI PREDICTION"

# the argument is the input files with its column number
python3 DDIbasedPPIprediction.py \
	--bacterial_input "Metaproteome_pfam_forDDI.txt" \
	--bacterial_id_col $bacterial_id_col \
	--bacterial_pf_col $bacterial_pf_col \
	--human_input "humanprots_pfam_forDDI.txt" \
	--human_id_col $human_id_col \
	--human_pf_col $human_pf_col

cp DDIpreds.txt $main_dir/output
mv DDIpreds_with_info.txt $main_dir/output

fi
############################
## Domain-motif interaction

if [ $DDInDMI = "DMI" ] || [ $DDInDMI = "ALL" ]; then


cd $pipe_dir/2.DMI/

cp $main_dir/user_inputs/$bacterial_proteins .
cp $main_dir/user_inputs/$human_receptors_DMI .

echo "----STARTING DMI PREDICTION"

# the output of DMI.py is MPDMIresult.tsv
python3 DMI.py \
	--bacterial_input $bacterial_proteins \
	--bacterial_id_col $bacterial_id_col \
	--bacterial_pf_col $bacterial_pf_col \
	--human_receptors_DMI $human_receptors_DMI


#########
## DMI prediction need to go for a structural filtering

cd $pipe_dir/3.Structural_filtering/structural_filtering/src

input3="$pipe_dir/2.DMI/MPDMIresult.tsv"

echo "----STARTING STRUCTURAL FILTERING"

python3 structural_filtering_prediction.py \
	--hmi_prediction $input3 \
	--resources ../resources \
	--results ../results

rm -rf ../resources/protein_sequences/*
echo "--- STRUCTURAL FILTERING FINISHED!\n Output file: DMI_filtered.csv"
cp ../results/idr_motifs.csv $main_dir/output/DMI_filtered.csv

fi

#### By this point, we will have:
### 1) a list of predicted DDI
### 2) a list of predicted and filtered DMI


######################################
######## STEP 3: TIE DIE COMPILATION

### Generating input file: to run TieDie using the predicted interactions as upstream input, we will run the following script, that will turn it on the ideal input
echo "--- GENERATING TieDie INPUT FROM PREDICTED INTERACTIONS"

bac_col_DMI=6
rec_col_DMI=1
bac_col_DDI=1
rec_col_DDI=2

input_DMI="$main_dir/output/DMI_filtered.csv"
input_DDI="$main_dir/output/DDIpreds.txt"


cd $pipe_dir/4.TieDie/ML_generating_input

python3 tiedie_input.py \
	$input_DMI \
	$bac_col_DMI \
	$rec_col_DMI \
	$input_DDI \
	$bac_col_DDI \
	$rec_col_DDI $DDInDMI

cp upstream.input $main_dir/output/Tie_Die_upstream.input #copy for the user too
echo "--- TieDie INPUT FINISHED!"


### Running TieDie
cd ../ML_executing

cp $main_dir/user_inputs/$target_genes_file ./downstream.input

echo "--- TieDie starting..."

python3 ../bin/tiedie -u upstream.input -d downstream.input -n pathway_$id_format.sif -s 1.0 --output_folder output_folder

cd output_folder/tiedie* $main_dir/output/
echo "--- TieDie FINISHED!!!! \n Output: tiedie.sif"

echo "--- MicrobioLink SIMULATION COMPLETED! \n THANKS FOR USING MicrobioLink :)"