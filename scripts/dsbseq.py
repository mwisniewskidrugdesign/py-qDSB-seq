import sys
import os
from typing import List
import subprocess
class DSBseq():
    def __init__(self,genome_name: str, chr_len: str,bowtie_index: str,enzyme_name: str, enzyme_type: int,enzyme_cutting_sites: str,DSB_reads: List, prefix: str, output_dir: str):
        self.genome_name = genome_name
        self.chr_len = chr_len
        self.bowtie_index = bowtie_index
        self.enzyme_name = enzyme_name
        self.enzyme_type = enzyme_type
        self.enzyme_cutting_sites = enzyme_cutting_sites
        self.DSB_reads = DSB_reads
        self.prefix = prefix
        self.output_dir = output_dir
        self.btt_dir = None
        self.mapping_params='-m1 -v1 -5 0 -3 0 -p2 -r'
    def pipeline(self,gates):
        '''Pipeline for mapping DSB-seq to reference genome'''

        if len(gates) != 3: # check if there are 3 gates for mapping, crerate_bedgraph and counting enzyme reads
            gates_error = '''
                Missing gates, please specify them:
                gates = [map_genome,create_bedgraph,count_enzyme_reads] 
            '''
            print(gates_error)
            sys.exit()
        else:
            map_genome = gates[0]
            create_bedgraph = gates[1]
            count_enzyme_reads = gates[2]
        btt_dir = self.output_dir + '/results/map_SE_to' + self.genome_name + '_btt'

        if map_genome:
            map_genome_text = '''
                Running: 
                    map to genome, create btt file, please don't terminate the running software.
                '''
            print(map_genome_text)
            self.mapping_se()
    def mapping_se(self,hits_dir='close_barcode'):
        mapping_se_text = '''
        Using:
            Genome name:    human,mouse,yeast,...
            Bowtie index:   bowtie_index
                            for example:
                            yeast qDSB-seq: /data/store/yizhu/my_databases/yeast/sc3_generate_G_MEC/sc3_generated_G_MEC.bowtie
                            yeast sc3: /data/store/yizhu/my_databases/yeast/sc2011/sc3.bowtie
                            human: /data/store/yizhu/my_databases/human/bowtie_index/hg19
                            mouse: /data/store/yizhu/my_databases/mouse/mm10/bowtie_index/mm10
            mapping_params: bowtie parameters
                            for example:
                            '-m1 -v1 -5 0 -3 10 -p2 -[fqr]'
            output_dir:     The output directory of all outputs
            bt_prefix:      The output prefix of .bt,.btt
            hits_dir:       The directory of hits files: no_barcode, close_barcode,distant_barcode
            DSB_reads:      List of R1 and R2 DSBseq reads
                            [R1,R2]
        '''

        mapping_params_list = self.mapping_params.split(' ')
        print(mapping_params_list)
        if len(self.DSB_reads) == 2:
        #mapping_command = ['bowtie2',self.bowtie_index,]
#smina_command=[settings.smina_tools_dir,'-r',self.protein_file,'-l',self.ligand_file,'--autobox_ligand',self.native_ligand_file,'--autobox_add','8','--exhaustiveness','32','--num_modes',str(no_modes),'-o',self.pdbqt_output_file,'--atom_terms',self.atom_terms_output_file,'--log',self.log_output_file,'--atom_term_data','--cpu','3','--min_rmsd_filter','0','--energy_range','10000']
        #docking = subprocess.run(smina_command, shell=False, capture_output=True, text=True)
       # print(docking.stderr)
       # print(docking.stdout)

            print('yo')


        elif len(self.DSB_reads) == 1:
            print('SE')
        else:
            print('chujnia')

