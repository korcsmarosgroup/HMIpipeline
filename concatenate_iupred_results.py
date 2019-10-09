import os
# Define the directory containing the files you are working with
#path = path
# Get all the files in that directory with the desired extension
files = [f for f in os.listdir(path)]
# specify output file
outfile =  open ("sum_iupredresults.txt","w")
for file in files:
    with open(path + '/' + file, 'r') as infile:
        for line in infile:
            #if ("#" not in line) and ("!" not in line) and ("identifier" not in line) and ("<" not in line) and (">" not in line) and ("(" not in line) and (")" not in line) and ("/" not in line) and (";" not in line) and ("}" not in line) and ("{" not in line) and (":" not in line) and ("False" in line):# for iupred               
            if "#" not in line:# for elm
                line = line.strip()
                outfile.write(file.split(".")[0] + " " + line + "\n")
outfile.close()
