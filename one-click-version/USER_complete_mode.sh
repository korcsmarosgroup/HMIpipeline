#!/bin/bash
########################################################
################### MicrobioLink 1.0 ###################
########################################################
##### With this script you will be able to run the #####
##### complete pipeline, including all the steps.  #####
##### Complete the variables above according with  #####
##### your data. 								   #####
########################################################

# Do not include space between the "=" and the string!
# Do id_format="uniprot" and not id_format= "uniprot"

###################
### INPUT FILES 

##1. BACTERIAL PROTEIN FILE
# Complete with the name of your bacterial proteins file. 
# It must have a column with its ID and other with its PFAM code.
# Complete with the number of the column correspondent with each one.
bacterial_proteins="Metaproteome.txt"
#ex: "Metaproteome.txt"
bacterial_column_id=1
#ex: 1
bacterial_column_pf=2
#ex: 2

##2. HUMAN PROTEIN FILE
# Complete with the name of your human proteins file. 

# If you will perform DDI prediction, your file must have a column with its ID and other with its PFAM code.
# Complete with the number of the column correspondent with each one.
human_proteins_DDI="humanDDI.txt"
#"humanDDI.txt"
human_column_id=1
#1
human_column_pf=2
#2

# If you will perform DMI prediction, your file must have a .fasta with the protein ID under your aminoacid sequence.
human_proteins_DMI="humanDMI.fasta"
#"humanDMI.fasta"



##3. Target_genes_file
# List of your target genes to TieDie execution.
# It must have the gene name in the 1th column, gene weight in the 2nd column and if it its status is + or - (up or downregulated, for example)
target_genes_file="Tie_Die_downstream.input"
#"Tie_Die_downstream.input"


###################
### PARAMETERS

DDInDMI="ALL"
#"ALL" or "DDI" or "DMI"

id_format="uniprot"
#"genename" or "uniprot"

###################
### COMMAND LINE
sh complete.sh $bacterial_proteins $bacterial_column_id $bacterial_column_pf $human_proteins_DDI $human_column_id $human_column_pf $human_proteins_DMI $target_genes_file $DDInDMI $id_format

#sh complete.sh 
#1 $bacterial_proteins 
#2 $bacterial_column_id 
#3 $bacterial_column_pf 
#4 $human_proteins_DDI 
#5 $human_column_id 
#6 $human_column_pf 
#7 $human_proteins_DMI 
#8 $target_genes_file 
#9 $DDInDMI 
#10$id_format