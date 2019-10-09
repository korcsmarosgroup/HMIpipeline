#!/bin/bash
#SBATCH -N 1                           # number of nodes
#SBATCH -n 1                           # number of tasks
#SBATCH -c 1                           # number of cores
#SBATCH -p ei-long                     # partition
#SBATCH --mem 50000                     # memory
#SBATCH -t 30-00:00                     # timelimit (D-HH:MM)
#SBATCH --mail-type=ALL              # mail me everything

source hpccore-5
source interproscan-5 

interproscan.sh -appl Pfam -i /tgac/workarea/group-gc/Paddy_all/2019/lejla/sequences.fasta

