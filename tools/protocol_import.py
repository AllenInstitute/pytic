import csv

'''
Requires user to remove header and extra new-lines in-between entries
'''


pfile =  open("tic_protocol.h", 'r')        # Copy file to leave original unaltered
ofile = open('pytic_protocol.py', 'w')
preader = csv.reader(pfile, delimiter=' ')
ofile.write("tic_constant = {\n")

for r in preader:
    ofile.write('\t\'' + r[1] + '\': ' + r[2] + ',\n')

ofile.write('}')
ofile.close()
pfile.close()