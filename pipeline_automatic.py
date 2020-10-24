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
        # het MSA bestand bestaat al
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
    return


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
    return


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
    return


def main():
    """ This pipeline is to be run in the terminal
    """
    try:
        # Het fasta bestand dat je gebruikt voor de msa
        fasta_input = argv[1]
        # De bestandsnaam waarin de msa wordt afgeschreven (zonder extensie)
        msa_output_arg = argv[2]
        # De naam voor de hmmsearch output bestanden (zonder extensie)
        hmmsearch_output_file = argv[3]
        # De naam voor het multiple fasta bestand met de fasta sequenties van je hmmsearch (zonder extensie)
        fasta_results_arg = argv[4]
        # De database waarin gezocht moet worden
        database = argv[5]
        # aantal iteraties dat moet worden gedaan
        max_iters = argv[6]

        results_folder = "./pipeline_results/"
        first_itter = True
        previous_fasta_output = ""
        for i in range(int(max_iters)):
            current_iter = i + 1
            current_result_folder = results_folder + "iter" + str(current_iter) + "_results/"
            # een map voor de huidige iteratie wordt aangemaakt, bijvoorbeeld ./pipeline_results/iter1_results/
            if os.path.isdir(current_result_folder):
                # output map voor iteratie bestaat al
                print("Output folder for current iteration already exists")
            else:
                os.makedirs(current_result_folder)  # maakt de directory

                # msa_output bestand wordt aangemaakt. Dit wordt gedaan door "het pad naar de map van de huidige
                # iteratie + de naam van het bestand + extensie" samen te plakken. Bijvoorbeeld:
                # bijvoorbeeld ./pipeline_results/iter1_results/test_msa.msa
                msa_output = current_result_folder + msa_output_arg + ".msa"

                if first_itter:
                    # wanneer het de eerste iteratie is, dan moet het fasta bestand dat in de command line is opgegeven
                    # worden gebruikt
                    mafft(fasta_input, msa_output)
                    first_itter = False
                else:
                    # wanneer het niet de eerste iteratie is, dan moet het fasta bestand dat bij de vorige iteratie
                    # is gemaakt, worden gebruikt. previous_fasta_output wordt verder op gedeclareerd
                    if os.path.isfile(previous_fasta_output):
                        mafft(previous_fasta_output, msa_output)
                    else:
                        print("Something went wrong with the previous iteration, no fasta_input found")

                # bestand waarna hmm profiel wordt geschreven
                hmmbuild_output = current_result_folder + msa_output_arg + ".hmm"

                # bestanden hmmsearch output
                hmmsearch_output_alignment = current_result_folder + hmmsearch_output_file + ".hmmsearch_alignment"
                hmmsearch_output_summary = current_result_folder + hmmsearch_output_file + ".hmmsearch_summary"

                hmmbuild(msa_output, hmmbuild_output)

                hmmsearch(hmmbuild_output, hmmsearch_output_alignment, hmmsearch_output_summary, database)

                fasta_results = current_result_folder + fasta_results_arg + ".fa"
                previous_fasta_output = fasta_results  # zodat het script weet waar het fasta bestand van de vorige
                # iteratie naar toe is gegaan
                hmmsearch_to_fasta(fasta_results, hmmsearch_output_alignment)

    except IndexError:
        print("Incorrect number of command line arguments."
              "\nUsage: python3 pipeline_automatic.py [fasta_input (.fasta format)] [msa_output (no extensions)] "
              "[hmmsearch_output (no extensions)] [fasta_results (no extensions)] [database] "
              "[number of iterations (int)]")
    except ValueError:
        print("Please give integer input for max_iteration argument")


main()
