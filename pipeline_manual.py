import os
from sys import argv


def mafft(fasta_input, msa_output):
    """ Calls the system to execute a command in the terminal to start MAFFT and does a MSA
    input:
    fasta_input - A file that contains the fasta sequences that you want to align
    msa_output - This is the name of the file that you want the MSA output file to have
    output: -
    """
    if os.path.isfile(msa_output):
        # msa bestand bestaat al
        print("MSA file already exists")
        pass
    else:
        e = os.system('/usr/bin/mafft --auto --inputorder "{}" > "{}"'.format(fasta_input, msa_output))
        print("MSA was successful")
    return


def hmmbuild(msa_input, hmmbuild_output):
    """ function that creates a hmm profile from a multiple sequence alignment
    input:
    msa_input - a file containing a multiple sequence alignment
    hmmbuild_output - name of file where hmm profile should be written to
    output: -
    """
    if not os.path.isfile(msa_input):
        # msa file bestaat niet
        print("Could not find MSA, mafft failed")
    elif os.path.isfile(hmmbuild_output):
        # hmmbuild output bestand bestaat al
        print("HMM file already exists")
        pass
    else:
        e = os.system("hmmbuild --amino {} {}".format(hmmbuild_output, msa_input))
        print("hmmbuild was successful")


def hmmsearch(hmm_input, hmmsearch_output_alignment, hmmsearch_output_summary, database):
    """ Function that searches a database with a hmm profile
    input:
    hmm_input - A file containing a hmm profile
    hmmsearch_output_alignment - A file where the MSA of the results should be written to
    hmmsearch_output_summary - A file where the results of the database search should be written to
    database - a file that functions as the database that will be searched against with the hmm profile
    output: -
    """
    if not os.path.isfile(hmm_input):
        # hmm profiel bestaat niet
        print("Could not find hmm profile, hmmbuild failed")
    elif os.path.isfile(hmmsearch_output_alignment or hmmsearch_output_summary):
        # de hmmsearch output bestanden bestaan al
        print("hmmsearch result files already exist")
    else:
        # voor het verkrijgen van de MSA
        e = os.system("hmmsearch --noali -A {} {} {}".format(hmmsearch_output_alignment, hmm_input, database))
        print("hmmsearch alignment file acquired successfully ")

        # voor de soort van BLAST output
        e = os.system("hmmsearch {} {} > {}".format(hmm_input, database, hmmsearch_output_summary))
        print("hmmsearch summary file acquired successfully")


def hmmsearch_to_fasta(fasta_results, hmmsearch_output):
    """ Converts the hmmsearch_output from stockholm to fasta using esl-reformat
    input:
    fasta_results - Name of the file the fasta sequences should be written to
    hmmsearch_output - A stockholm format file containing the results of a hmmsearch
    output: -
    """
    if not os.path.isfile(hmmsearch_output):
        # Hmmsearch output bestaat niet
        print("Could not find hmmsearch alignment file, conversion failed")
        pass
    elif os.path.isfile(fasta_results):
        # Er is al een bestand met deze naam
        print("fasta_results file already exists")
        pass
    else:
        e = os.system("./esl-reformat -o {} -u fasta {}".format(fasta_results, hmmsearch_output))
        print("hmmsearch output successfully converted to fasta format for new iteration")


def main():
    """ This pipeline is to be run in the terminal
    """
    try:
        # Het fasta bestand dat je gebruikt voor de msa
        fasta_input = argv[1]
        # De bestandsnaam waarin de msa wordt afgeschreven (zonder extensie)
        msa_output = argv[2]
        # De naam voor de hmmsearch output bestanden (zonder extensie)
        hmmsearch_output_file = argv[3]
        # De database waarin gezocht moet worden
        database = argv[4]
        # De naam voor het multiple fasta bestand met de fasta sequenties van je hmmsearch (zonder extensie)
        fasta_results = argv[5]

        mafft(fasta_input, msa_output)

        # bestand hmmbuild profiel output
        hmmbuild_output = msa_output + ".hmm"
        # bestanden hmmsearch output
        hmmsearch_output_alignment = hmmsearch_output_file + ".hmmsearch_alignment"
        hmmsearch_output_summary = hmmsearch_output_file + ".hmmsearch_summary"

        hmmbuild(msa_output, hmmbuild_output)

        hmmsearch(hmmbuild_output, hmmsearch_output_alignment, hmmsearch_output_summary, database)

        fasta_results = fasta_results + ".fa"
        hmmsearch_to_fasta(fasta_results, hmmsearch_output_alignment)

    except IndexError:
        print("Incorrect number of command line arguments."
              "\nUsage: python3 pipeline_manual.py [fasta_input (fasta format)] [msa_output (no extensions)] "
              "[hmmsearch_output (no extensions)] [database] [fasta_results (no extensions)]")


main()
