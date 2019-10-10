# this script uncovers all possible paths of a given length from a given directed network for given set of start nodes and a given set of stop nodes
source = []
target = []
ints = []
# specify start node list
with open ("start_node_list.txt") as infile1:
    for line1 in infile1:
        line1 = line1.strip()
        source.append(line1)
# specify stop node list
with open ("stop.txt") as infile2:
    for line2 in infile2:
        line2 = line2.strip()
        target.append(line2)
# specify directed network
with open ("nets.txt") as infile3:
    for line3 in infile3:
        line3 = line3.strip()
        cells3 = line3.split()
        n1 = cells3[0]
        n2 = cells3[1]
        ints.append([n1,n2])


paths = []
# specify number of steps between the start and stop nodes
# for example maxstep = 2 indicates the presence of one intermediary node between the start and stop nodes
maxstep = 2

for s in source:
    paths.append([s])

for n in range(maxstep-1):
    pathsext = []
    for path in paths:
        laststep = path[-1]
        for i in ints:
            if laststep == i[0]:
                newpath = list(path)
                newpath.append(i[1])
                pathsext.append(newpath)
                #print(newpath)
    for path in pathsext:
        if path not in paths:
            paths.append(path)

# specify output file to store the recovered paths
outfile = open ("chains.txt","w")
for path in paths:
    if path[-1] in target:
        outfile.write("\t".join(path) + "\n")
outfile.close()
