#!/bin/bash
########################################################
################### MicrobioLink 1.0 ###################
########################################################
##### With this script you will be able to run     #####
##### separated steps of the pipeline.             #####
##### Complete the variables above according with  #####
##### your data.								   #####
##### The instrucions about how	to complete the    #####
##### variables according to the step you want to  #####
##### perform can be found in the bottom of this   #####
##### file and more details in the README file.    #####
########################################################

echo "------------------------------------------------------------------------------"
echo "--- MAKE SURE THAT YOU ARE CONNECTED TO THE VIRTUAL ENVIRONMENT OR DOCKER. ---" 
echo "--- CHECK THE README FILE FOR MORE INFORMATION -------------------------------"
echo "------------------------------------------------------------------------------"

###################
# The following parameters and input files will depend on the step you will perform.
# See the instructions for it in the bottom of this file and more details in the README file..

# The input files must be in the folder user_inputs/
# The output files will be found in the folder output/

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


#########################################
### COMMAND LINE. YOU MUST NOT CHANGE IT!
sh stepbystep.sh $step $id_format $input_file1 $col_id1 $col_pf1 $input_file2 $col_id2 $col_pf2 

 
<< USING_THE_VARIABLES_FOR_EACH_STEP

Do not include space between the "=" and the string!
Do id_format="uniprot" and not id_format= "uniprot"

#### DDI:
# input_file1= bacterial proteins file
# col_id1= number of bacterial protein ID column
# col_pf1= number of bacterial protein PFAM column
# input_file2= host protein file
# col_id2= number of host protein ID column
# col_pf2= number of host protein PFAM column

#### DMI:
# input_file1= bacterial proteins file
# col_id1= number of bacterial protein ID column
# col_pf1= number of bacterial protein PFAM column
# input_file2= host protein sequences fasta file
# col_id2=0
# col_pf2=0

#### STRUCTURAL FILTERING:
# input_file1= DMI file
# col_id1=0
# col_pf1=0
# input_file2=0
# col_id2=0
# col_pf2=0

#### TIE DIE INPUT GENERATOR
# input_file1= Interactions file
# col_id1= number of bacterial protein ID column
# col_pf1= number of host protein ID column
# input_file2=0
# col_id2=0
# col_pf2=0

#### TIE DIE EXECUTOR
# input_file1=upstream file
# col_id1=0
# col_pf1=0
# input_file2=downstream file
# col_id2=0
# col_pf2=0

USING_THE_VARIABLES_FOR_EACH_STEP
