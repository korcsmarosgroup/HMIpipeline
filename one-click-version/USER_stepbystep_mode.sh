#!/bin/bash
########################################################
################### MicrobioLink 1.0 ###################
########################################################
##### With this script you will be able to run     #####
##### separated steps of the pipeline.             #####
##### Complete the variables above according with  #####
##### your data. 								   #####
########################################################

# Do not include space between the "=" and the string!
# Do id_format="uniprot" and not id_format= "uniprot"

###################
# The following parameters and input files will depend on the step you will perform.

## GENERAL PARAMETERS
step="tiedie"
#"DDI" or "DMI" or "structural_filtering" or "tiedie_input" or "tiedie"

id_format="uniprot"
#"genename" or "uniprot"

input_file1="Tie_Die_upstream.input"
col_id1=0
col_pf1=0
input_file2="Tie_Die_downstream.input"
col_id2=0
col_pf2=0

###################
### COMMAND LINE
sh stepbystep.sh $step $id_format $input_file1 $col_id1 $col_pf1 $input_file2 $col_id2 $col_pf2 
