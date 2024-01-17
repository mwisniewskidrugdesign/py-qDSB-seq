#!/bin/bash


if [ "$#" -lt 2 ]; then
    echo '''
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
    exit 1
fi

USAGE="$0 $1 $2 $3 [-s <s> -r <r> -g <g> -f <f> -i <i> -e <e> -t <t> -c <c> -b <b> -p <p> -o <o>]"

DSB_reads=$1
gDNA_reads_1=$2
gDNA_reads_2=$3
shift 3

sample_name="unknown"
group_sample="unknown"
genome_name="genome"
bowtie_index=""
genome_sequence=""
enzyme_name="unknown"
enzyme_type="3"
enzyme_cutting_sites=""
background=""
prefix="output"
output_dir=''


while getopts 's:r:g:f:i:e:t:c:b:p:o:' opt ; do
	case $opt in
		s) sample_name="$OPTARG";;
		r) group_sample="$OPTARG" ;;
		g) genome_name="$OPTARG" ;;
		f) genome_sequence="$OPTARG" ;;
		i) bowtie_index="$OPTARG" ;;
		e) enzyme_name="$OPTARG" ;;
		t) enzyme_type="$OPTARG" ;;
		c) enzyme_cutting_sites="$OPTARG" ;;
		b) background="$OPTARG" ;;
		p) prefix="$OPTARG" ;;
    o) output_dir="$OPTARG" ;;
		\?) echo "Invalid option: -$OPTARG"; exit 1 ;;
		:) echo "Option -$OPTARG requires an argument."; exit 1 ;;
	esac
done

# Dostęp do zmiennych
echo "DSB_reads: $DSB_reads"
echo "gDNA_reads_1: $gDNA_reads_1"
echo "gDNA_reads_2: $gDNA_reads_2"
echo "sample_name: $sample_name"
echo "group_sample: $group_sample"
echo "genome_name: $genome_name"
echo "genome_sequence: $genome_sequence"
echo "bowtie_index: $bowtie_index"
echo "enzyme_name: $enzyme_name"
echo "enzyme_type: $enzyme_type"
echo "enzyme_cutting_sites: $enzyme_cutting_sites"
echo "background: $background"
echo "prefix: $prefix"
echo "output_directory: $output_dir"

output_dir=$output_dir'/results'
mkdir $output_dir

# 1) create genome sequence length file and genome sequence length bed file, if there is no genome sequence :c

chr_length=${#genome_sequence}
if [ -n "$genome_sequence" ]; then
  genome_sequence_output_dir=$output_dir'/genome_sequence'
  mkdir $genome_sequence_output_dir

  genome_sequence_length_file=$genome_sequence_output_dir'/genome_sequence.length'
  genome_sequence_length_bed_file=$genome_sequence_output_dir'/genome_sequence.length.bed'

	python3 scripts/fasta_length.py "$genome_sequence" >$genome_sequence_length_file 2>$genome_sequence_length_bed_file
fi

# 2) map DSB sequencing data to genome, and call depth

python3 process_DSB-seq_data.py $genome_name $chr_length $bowtie_index $enzyme_name $enzyme_type $enzyme_cutting_sites $DSB_reads $prefix $output_dir












