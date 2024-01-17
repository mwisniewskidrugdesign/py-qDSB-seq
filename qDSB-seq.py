import sys
import os
import argparse
from scripts import fasta_length,dsbseq


software_description='''
    qDSB-seq.pl performs quantitative DSB sequencing analysis, including:
    
	1) map DSB sequencing data to genome, and call depth
	2) map gDNA sequencing data to genome, and calculate enzyme cutting efficiency
	3) calculate DSB frequencies per cell on the whole genome or specific locations 

	Usage: bash $0 <DSB reads> <gDNA reads R1> <gDNA reads R2> [options] 

	    -s CHARACTER	sample name
	    -r CHARACTER  group of the sample, for example, G1 or S
	    -g CHARACTER	genome name
	    -f CHARACTER  genome sequence in fasta format
	    -i CHARACTER	genome bowtie index
	    -e CHARACTER	enzyme name
	    -t CHARACTER  enzyme type
	    -c CHARACTER  enzyme cutting sites in BED format
	    -b CHARACTER  backgrond coordinates on genome to remove background noise from cutting efficiency calculation
	    -p CHARACTER  output prefix
	    -o CHARACTER  output direcctory

	Please contact Dr. Yingjie Zhu for any questions on the code yizhu\@utmb.edu

'''

### PARAMETERS ###
DSB_reads = list(sys.argv[1])
gDNA_reads_1 = sys.argv[2]
gDNA_reads_2 = sys.argv[3]
sample_name="unknown"
group_sample="unknown"
genome_name="genome"
genome_sequence=""
bowtie_index=""
enzyme_name="unknown"
enzyme_type="3"
enzyme_cutting_sites=""
background=""
prefix="output"
output_dir=""

### ADD PARAMETERS ###

parser = argparse.ArgumentParser(description=software_description)

parser.add_argument('-s', '--sample', dest='sample_name', required=False, help='Name of the sample')
parser.add_argument('-r', '--group', dest='group_sample', required=False,  help='Name of the sample\'s group, for example G1 or S')
parser.add_argument('-g', '--genome', dest='genome_name', required=False, help='Name of the genome, for example hg38')
parser.add_argument('-f', '--genome_seq', dest='genome_sequence', required=True, help='Genome sequence in fasta format')
parser.add_argument('-i', '--bowtie_idx', dest='bowtie_index', required=True,help='Genome bowtie index files')
parser.add_argument('-e', '--enzyme', dest='enzyme_name',required=False, help='Name of the enzyme, for example SgrDi')
parser.add_argument('-t', '--enzyme_type', dest='enzyme_type',required=False, help='Type of the enzyme, for example ...')
parser.add_argument('-c', '--cutting', dest='enzyme_cutting_sites',required=True, help='Enzyme cutting sites in BED format')
parser.add_argument('-b', '--background', dest='background',required=True, help='backgrond coordinates on genome to remove background noise from cutting efficiency calculation')
parser.add_argument('-p', '--prefix', dest='prefix',required=False, help='output prefix name')
parser.add_argument('-o', '--output_dir', dest='output_dir',required=True, help='Absolute output directory')


#e = parser.parse_args(sys.argv)
args = parser.parse_args(sys.argv[4:])

if args.sample_name:
    sample_name = args.sample_name
if args.group_sample:
    group_sample = args.group_sample
if args.genome_name:
    genome_name = args.genome_name
genome_sequence = args.genome_sequence
bowtie_index = args.bowtie_index
if args.enzyme_name:
    enzyme_name = args.enzyme_name
if args.enzyme_type:
    enzyme_type = args.enzyme_type
enzyme_cutting_sites = args.enzyme_cutting_sites
background = args.background
if args.prefix:
    prefix = args.prefix
output_dir = args.output_dir

print("DSB_reads:\t", DSB_reads)
print("gDNA_reads_1:\t", gDNA_reads_1)
print("gDNA_reads_2:\t", gDNA_reads_2)
print("sample_name:\t", sample_name)
print("group_sample:\t", group_sample)
print("genome_name:\t", genome_name)
print("genome_sequence:\t", genome_sequence)
print("bowtie_index:\t", bowtie_index)
print("enzyme_name:\t", enzyme_name)
print("enzyme_type:\t", enzyme_type)
print("enzyme_cutting_sites:\t", enzyme_cutting_sites)
print("background:\t", background)
print("prefix:\t", prefix)
print("output_directory:\t", output_dir)



output_dir=output_dir+'/results'
os.makedirs(output_dir,exist_ok=True)



# 1) create genome sequence length file and genome sequence length bed file, if there is no genome sequence :c

chr_length = len(genome_sequence) if genome_sequence else 0
if genome_sequence:

    genome_sequence_output_dir = os.path.join(output_dir, 'genome_sequence')
    length_output = os.path.join(genome_sequence_output_dir,'genome_sequence.length')
    bed_output = os.path.join(genome_sequence_output_dir,'genome_sequence.length.bed')

    os.makedirs(genome_sequence_output_dir, exist_ok=True)

    fasta_length.main(genome_sequence,length_output,bed_output)


# 2) map DSB sequencing data to genome, and call depth

    aphi = dsbseq.DSBseq(genome_name,chr_length,bowtie_index,enzyme_name,enzyme_type,enzyme_cutting_sites,DSB_reads,prefix,output_dir)
    aphi.pipeline(gates=[True,True,True])


#py-qDSB-seq % python3 qDSB-seq.py a b c -s sample_value -r group_value -g genome_value -f example/reference_genome/test.reference_genome.fas -i bowtie_value -e enzyme_value -t enzyme_type_value -c cutting_type_value -b background_value -p prefix_value -o dupa
