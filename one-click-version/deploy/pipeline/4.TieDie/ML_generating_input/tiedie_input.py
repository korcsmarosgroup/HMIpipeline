import sys


##### Function that import file. 
#### inte_file = input file name
#### bact_prot = column number containing bacterial proteins
#### receptor = column number containing receptors
#### header = True if there are headers in the file
def DicInteractions(inte_file,bact_prot,receptor,header=False):
	with open (inte_file) as inte_list:
		list_inte=[a.strip().split() for a in inte_list.readlines()]
		if header == True:
			list_inte=list_inte[1:]
		list_inte=[[a[bact_prot],a[receptor]] for a in list_inte]
		dic_br=dict([(a[1],set()) for a in list_inte]) #dictionary bacterial protein = receptor
		for inte in list_inte:
			dic_br[inte[1]].add(inte[0])
	return dic_br


DMI_file=sys.argv[1]
DMI_bact_prot_col=int(sys.argv[2])-1
DMI_receptor_col=int(sys.argv[3])-1

DDI_file=sys.argv[4]
DDI_bact_prot_col=int(sys.argv[5])-1
DDI_receptor_col=int(sys.argv[6])-1

DDInDMI=sys.argv[7]

if DDInDMI == "ALL":
	dDMI=DicInteractions(DMI_file, DMI_bact_prot_col,DMI_receptor_col,True)
	dDDI=DicInteractions(DDI_file, DDI_bact_prot_col,DDI_receptor_col)

elif DDInDMI == "DDI":
	dDMI={}
	dDDI=DicInteractions(DDI_file, DDI_bact_prot_col,DDI_receptor_col)
else:
	dDDI={}
	dDMI=DicInteractions(DMI_file, DMI_bact_prot_col,DMI_receptor_col,True)

### Count with how many bacterial proteins each receptor interacts and merge into a dictionary
#dict_bac_rec = {}
all_rec = set(dDMI.keys()).union(set(dDDI.keys()))

dDDI_count={a:len(dDDI[a]) for a in dDDI.keys()}
dDMI_count={a:len(dDMI[a]) for a in dDMI.keys()}

with open('upstream.input','w') as outfile:
	for rec in all_rec:
		if rec in dDDI and rec in dDMI:
			#dict_bac_rec[rec] = len(dDDI[rec])+len(dDMI[rec])
			outfile.write(f"{rec}\t{len(dDDI[rec])+len(dDMI[rec])}\t+\n")
		else:
			if rec in dDDI:
				#dict_bac_rec[rec] = len(dDDI[rec])
				outfile.write(f"{rec}\t{len(dDDI[rec])}\t+\n")
			else:
				outfile.write(f"{rec}\t{len(dDMI[rec])}\t+\n")

	 
