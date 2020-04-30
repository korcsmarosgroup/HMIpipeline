# make a dictionary from ddi-s for faster serch
DDI = {}
with open('pfam_interactions.txt') as ddi_file:
    for line in ddi_file:
        line = line.strip()
        cell = line.split()
        # add ddi to dictionary like: pfam1;pfam2 and pfam2;pfam1 because undirected
        ddi_forward = "%s;%s" % (cell[0], cell[1])
        ddi_reverse = "%s;%s" % (cell[1], cell[0])
        DDI[ddi_forward] = True
        DDI[ddi_reverse] = True

bac_file = []
with open ('Metaproteome_pfam_forDDI.txt') as f:
    for line in f:
        bac_file.append(line.strip().split())
human_file = []
with open ('humanprots_pfam_forDDI.txt') as f:
    for line in f:
        human_file.append(line.strip().split())

outfile = open ('DDIpreds_metaproteome.txt', 'w')
infile1 = open ('Metaproteome_pfam_forDDI.txt')
infile2 = open ('humanprots_pfam_forDDI.txt')

i = 0
for cells1 in bac_file:
    for cells2 in human_file:
        i += 1
        bacpfam = cells1[1]
        #print(bacpfam)
        humanpfam = cells2[1]
        #print(humanpfam)
        ddi_test = "%s;%s" % (bacpfam, humanpfam)
        #print(ddi_test)
        if ddi_test in DDI:
            outfile.write("\t".join(cells1) + ";" + "\t".join(cells2) + "\n" )
print(i)
