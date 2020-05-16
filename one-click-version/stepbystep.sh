#!/bin/bash

###########################################################################
###########################################################################
#### MicrobioLink pipeline
###########################################################################

#sh pipeline_execution.sh "Metaproteome.txt" 1 2 "humanDDI.txt" 1 2 "humanDMI.fasta" "Tie_Die_downstream.input" ALL uniprot


### PASTE ABOVE THE NAME OF YOUR INPUTS:

step=$1
#"DDI" or "DMI" or "structural_filtering" or "tiedie_input" or "tiedie"
id_format=$2
#"genename" or "uniprot"


input_file1=$3
col_id1=$4
col_pf1=$5

input_file2=$6
col_id2=$7
col_pf2=$8

#"genename" or "uniprot"

###
main_dir="$(pwd)"
pipe_dir="$main_dir/deploy/pipeline"


########################################################
### STEP 1: INTERACTION PREDICTION

############################
# Domain-domain interaction

cd user_inputs

if [ $step = "DDI" ]; then

cp $input_file1 $pipe_dir/1.DDI/Metaproteome_pfam_forDDI.txt
cp $input_file2 $pipe_dir/1.DDI/humanprots_pfam_forDDI.txt

cd $pipe_dir/1.DDI/
echo "----STARTING DDI PREDICTION"
python3 DDIbasedPPIprediction.py "Metaproteome_pfam_forDDI.txt" $col_id1 $col_pf1 "humanprots_pfam_forDDI.txt" $col_id2 $col_pf2 ### the argument is the input files with its column number
cp DDIpreds.txt $main_dir/outputs
mv DDIpreds_with_info.txt $main_dir/outputs

fi

############################
## Domain-motif interaction

if [ $step = "DMI" ]; then

cd $main_dir/user_inputs

cp $input_file1 $pipe_dir/2.DMI/Metaproteome_pfam.txt
cp $input_file2 $pipe_dir/2.DMI/human_receptors.fasta

cd $pipe_dir/2.DMI/

echo "----STARTING DMI PREDICTION"
python3 DMI.py "Metaproteome_pfam.txt" $col_id1 $col_pf1 "human_receptors.fasta"
# the output of DMI.py is MPDMIresult.tsv
fi


#########
## Structural filtering

if [ $step = "structural_filtering" ]; then

cd $pipe_dir/3.Structural_filtering/structural_filtering/src

cp $main_dir/user_inputs/$input_file1 .

echo "----STARTING STRUCTURAL FILTERING"
python3 structural_filtering_prediction.py --hmi_prediction $input_file1 --resources ../resources --results ../results
rm -rf ../resources/protein_sequences/*
echo "--- STRUCTURAL FILTERING FINISHED!\n Output file: DMI_filtered.csv"
cp ../results/idr_motifs.csv $main_dir/outputs/DMI_filtered.csv

fi

#### By this point, we will have:
### 1) a list of predicted DDI
### 2) a list of predicted and filtered DMI



######################################
######## STEP 3: TIE DIE COMPILATION

### Generating input file: to run TieDie using the predicted interactions as upstream input, we will run the following script, that will turn it on the ideal input

if [ $step = "tiedie_input" ]; then

echo "--- GENERATING TieDie INPUT FROM PREDICTED INTERACTIONS"

#The input will be the predicted interactions. 
#DMI_file=sys.argv[1]
cd $pipe_dir/4.TieDie/ML_generating_input
cp $main_dir/user_inputs/$input_file1 ./input_generate

python3 tiedie_input.py 0 0 0 input_generate $col_id1 $col_pf1 DDI
cp upstream.input $main_dir/outputs/Tie_Die_upstream.input #copy for the user too
echo "--- TieDie INPUT FINISHED!"
fi

### Running TieDie

if [ $step = "tiedie" ]; then


cd $pipe_dir/4.TieDie/ML_executing

cp $main_dir/user_inputs/$input_file1 ./upstream.input
cp $main_dir/user_inputs/$input_file2 ./downstream.input

python3 ../bin/tiedie -u upstream.input -d downstream.input -n pathway_$id_format.sif -s 1.0 --output_folder output_folder

cd output_folder/
cp tiedie.sif $main_dir/outputs/

echo "--- TieDie FINISHED!!!!"
echo "-- Output: tiedie.sif"

fi
