# Course5_project pipeline

This pipeline takes a fasta file and makes an msa, then uses hmmbuild to create a hmmprofile and searches a given database to find more sequences matching the profile. Finally it also makes a fasta file from the hmmsearch results so it can be used again
input:
- fasta file
- database
output:
- msa file
- hmmbuild output file
- hmmsearch alignment file
- hmmsearch summary file
- new fasta file

Download msa_pipeline.py and all 4 of the esl-reformat files

To test also download globins.fasta and globins45.fa

# To use the pipeline for own use, make sure to have a fasta file to start with and a database to search in using hmmsearch,
# also make sure that every file is in the same directory.

# This pipeline is to be run in the terminal:
# Usage: python3 msa_pipeline.py [fasta_input (fasta format)] [msa_output (no extensions)] [hmmsearch_output (no extensions)] [database] [fasta_results (no extensions)]

