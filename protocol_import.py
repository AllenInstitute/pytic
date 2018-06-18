import csv

'''
requires suer to remove header and extra \n in-between entries
'''

# pfile =  open("C:\\Users\\danc\\dev\\tic\\include\\tic_protocol.h", 'r')
pfile =  open("tic_protocol.h", 'r') # copy file to leave original unaltered
ofile = open('pytic_protocol.py', 'w')
preader = csv.reader(pfile, delimiter=' ')
ofile.write("tic_constant = {\n")

for r in preader:
    ofile.write('\t\'' + r[1] + '\': ' + r[2] + ',\n')

ofile.write('}')
ofile.close()
pfile.close()