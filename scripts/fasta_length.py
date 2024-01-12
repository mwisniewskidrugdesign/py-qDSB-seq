import re
import sys
import os
import re

arguments = len(sys.argv) - 1 # subtract one to skip the script name

if arguments < 0:
    print('Usage: python3',sys.argv[0],'<fasta>\n')
    sys.exit()

input = sys.argv[1]

def fasta_length(fasta):
    name = ''
    seq = ''
    length = 0

    with open(fasta,'r') as infile:
        line = infile.readline()
        while line:
            line = line.rstrip('\n').rstrip('\r')

            if line.startswith('>') and (match := re.match(r'^>(\S+)', line)):
                if seq:
                    length += len(seq)
                    name = name.split()[0]
                    print(f"{name}\t{length}")
                    print(f"{name}\t1\t{length}", file=sys.stderr)
                    seq = ''

                name = match.group(1)
                length = 0

            elif infile.tell() == os.fstat(infile.fileno()).st_size:
                seq += line.replace(' ', '')

                if seq:
                    length += len(seq)
                    name = name.split()[0]
                    print(f"{name}\t{length}")
                    print(f"{name}\t1\t{length}", file=sys.stderr)
                    seq = ''

            elif line[0].isalpha():
                seq += line.replace(' ', '')

            line = infile.readline()

def process_directory(directory_path):
    with os.scandir(directory_path) as entries:
        for entry in entries:
            if entry.is_file() and (entry.name.endswith(('.fa','.fna','.fasta','.gb'))):
                fasta_length(entry.path)

def main(input_path):
    if os.path.isdir(input_path):
        process_directory(input_path)
    else:
        fasta_length(input_path)


main(input)