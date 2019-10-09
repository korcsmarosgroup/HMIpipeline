# make a dictionary from the gold-standard domain-domain interactions (from the DOMINE datbaase for example)
DDI = {}
with open('goldstandard_pfam_interactions.txt') as ddi_file:
    for line in ddi_file:
        line = line.strip()
        cell = line.split()
        # add ddi to dictionary like: pfam1;pfam2 and pfam2;pfam1 because undirected
        ddi_forward = "%s;%s" % (cell[0], cell[1])
        ddi_reverse = "%s;%s" % (cell[1], cell[0])
        DDI[ddi_forward] = True
        DDI[ddi_reverse] = True
# specify file with list of bacterial proteins and their annotated domains
bac_file = []
with open ('bacterialproteins_withdomains.txt') as f:
    for line in f:
        bac_file.append(line.strip().split())
# specify file with list of human (host) proteins and their annotated domains
human_file = []
with open ('hostproteins_withdomains.txt’) as f:
    for line in f:
        human_file.append(line.strip().split())
# specify output file in which the predicted protein-protein interactions will be stored pair-wise. The output will also contain information on the domains mediating the putative interactions. 
outfile = open ('output.txt','w')
infile1 = open ('bacterialproteins_withdomains.txt')
infile2 = open ('hostproteins_withdomains.txt')

i = 0
for cells1 in bac_file:
    for cells2 in human_file:
        i += 1
        bacpfam = cells1[1]
        #print(bacpfam)
        humanpfam = cells2[4]
        #print(humanpfam)
        ddi_test = "%s;%s" % (bacpfam, humanpfam)
        #print(ddi_test)
        if ddi_test in DDI:
            outfile.write("\t".join(cells1) + ";" + "\t".join(cells2) + "\n" )
            outfile.flush()
            outfile.close()
