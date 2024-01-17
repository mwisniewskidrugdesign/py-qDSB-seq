import re
import sys
import os
import re
# dodac opis
def fasta_length(fasta,length_output,bed_output):
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
                    print(f"{name}\t{length}", file=open(length_output,'a'))
                    print(f"{name}\t1\t{length}", file=open(bed_output,'a'))
                    seq = ''

                name = match.group(1)
                length = 0

            elif infile.tell() == os.fstat(infile.fileno()).st_size:
                seq += line.replace(' ', '')

                if seq:
                    length += len(seq)
                    name = name.split()[0]
                    print(f"{name}\t{length}", file=open(length_output,'a'))
                    print(f"{name}\t1\t{length}", file=open(bed_output,'a'))
                    seq = ''

            elif line[0].isalpha():
                seq += line.replace(' ', '')

            line = infile.readline()

def process_directory(directory_path,length_output,bed_output):
    with os.scandir(directory_path) as entries:
        for entry in entries:
            if entry.is_file() and (entry.name.endswith(('.fa','.fna','.fasta','.gb'))):
                fasta_length(entry.path,length_output,bed_output)

def main(input_path,length_output,bed_output):
    if os.path.isdir(input_path):
        process_directory(input_path,length_output,bed_output)
    else:
        fasta_length(input_path,length_output,bed_output)
