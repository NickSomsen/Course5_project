# Course5_project pipeline

This pipeline takes a fasta file and makes an msa, then uses hmmbuild to create a hmmprofile and searches a given database to find more sequences matching the profile. Finally it also makes a fasta file from the hmmsearch results so it can be used again. You can either start every iteraion manually (pipeline_manual.py), or specify the amount of iterations the pipeline should do (pipeline_automatic.py).

input:
- fasta file
- database
- max number of iterations when using pipeline_automatic.py

output:
- msa file
- hmmbuild output file
- hmmsearch alignment file
- hmmsearch summary file
- new fasta file

Download pipeline_manual.py, pipeline_automatic.py and all 4 of the esl-reformat files.

To test also download globins.fasta and globins45.fa from the test_files folder

To use the pipeline for own use, make sure to have a fasta file to start with and a database to search in using hmmsearch,
also make sure that every file is in the same directory as the script.

This pipeline is to be run in the terminal:
- Usage pipeline_manual.py: python3 pipeline_manual.py [fasta_input (fasta format)] [msa_output (no extensions)] [hmmsearch_output (no extensions)] [database] [fasta_results (no extensions)]
- Usage pipeline_automatic.py: python3 pipeline_automatic.py [fasta_input (.fasta format)] [msa_output (no extensions)] [hmmsearch_output (no extensions)] [fasta_results (no extensions)] [database] [number of iterations (int)]")
