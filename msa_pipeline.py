import os
import subprocess
from sys import argv


def mafft(fasta_input, msa_input):
    """ Calls the system to execute a command in the terminal to start MAFFT and does a MSA
    input:
    fasta_input - A file that contains the fasta sequences that you want to align
    msa_input - This is the name of the file that you want the MSA output file to have
    output: -
    """
    if os.path.isfile(msa_input):
        print("MSA file already exists")
        pass
    else:
        cmd = '/usr/bin/mafft --auto --inputorder "{}" > "{}"'.format(fasta_input, msa_input)
        e = subprocess.check_call(cmd, shell=True)
        print("MSA was successful")
    return


def hmmbuild(msa_input, hmmbuild_output):
    """ function that creates a hmm profile from a multiple sequence alignment
    input:
    msa_input - a file containing a multiple sequence alignment
    hmmbuild_output - name of file where hmm profile should be written to
    output: -
    """
    # replace_header(msa_input)
    # Alleen nodig als de input clustal format is.
    # Als de eerste iteratie is geweest, hoeft deze functie niet meer te worden aangeroepen denk ik

    if os.path.isfile(hmmbuild_output):  # file bestaat al
        print("HMM file already exists")
        pass
    else:
        e = os.system("hmmbuild --amino {} {}".format(hmmbuild_output, msa_input))
        print("hmmbuild was successful")


def replace_header(msa_input):
    """ Function that replaces the original file header, with a compatible header
    input:
    msa_input - A file containing a multiple sequence alignment
    output: -
    """
    with open(msa_input, "r") as inFile:
        all_lines = inFile.readlines()
    # Net als t-coffee, gaf hmmbuild ook een error dat hij de clustal header niet herkent. Ik heb toen gewoon weer die
    # Header van het voorbeeld van t-coffee gepakt,
    # Die wordt dan in het bestand gezet, in plaats van de originele header
    all_lines[0] = all_lines[0].replace(all_lines[0], "CLUSTAL W (1.82) multiple sequence alignment\n")

    with open(msa_input, "w") as inFile:
        # Het bestand wordt overschreven met de vervangende header. Dit kost dus wel wat tijd bij grotere bestanden,
        # Maar na de eerste iteratie hoeft dit niet meer te worden gedaan,
        # Omdat de resultaten dan wel een goede header hebben
        # (Dit kun je misschien reguleren met een boolean, maar je kunt misschien ook de header in het bestand
        # Handmatig één keer aanpassen en dan deze hele functie gewoon weghalen).
        for line in all_lines:
            inFile.write(line)


def hmmsearch(hmm_input, hmmsearch_output_alignment, hmmsearch_output_summary, database):
    """ Function that searches a database with a hmm profile
    input:
    hmm_input - A file containing a hmm profile
    hmmsearch_output_alignment - A file where the MSA of the results should be written to
    hmmsearch_output_summary - A file where the results of the database search should be written to
    database - a file that functions as the database that will be searched against with the hmm profile
    output: -
    """
    if os.path.isfile(hmm_input):
        # het hmm profiel bestaat, hmmsearch kan worden uitgevoerd
        if os.path.isfile(hmmsearch_output_alignment) or os.path.isfile(hmmsearch_output_summary):
            # De output bestanden bestaan al
            print("hmmsearch result files already exist")
            pass
        else:
            # hmmsearch kun je op meerdere manieren doen, en beide geven interessante input:
            # de eerste manier waarbij je, als het goed is, een MSA van de resultaten terug krijgt
            e = os.system("hmmsearch -A {} {} {}".format(hmmsearch_output_alignment, hmm_input, database))
            print("hmmsearch alignment file acquired successfully ")

            # de tweede manier waarbij je een duidelijk overzicht krijgt van elke alignment, en onder andere het totaal
            # aantal hits
            e = os.system("hmmsearch {} {} > {}".format(hmm_input, database, hmmsearch_output_summary))
            print("hmmsearch summary file acquired successfully")

    else:
        print("Could not find hmm profile, hmmsearch failed")


def main():
    """ This pipeline is to be run in the terminal
    """
    try:
        fasta_input = argv[1]
        # Het fasta bestand dat je gebruikt voor de msa
        msa_input = argv[2]
        # Het de bestands naam waarin de msa wordt afgeschreven (zonder extensie)
        hmmsearch_output_file = argv[3]
        # De naam voor de hmmsearch output bestanden (zonder extensie)
        database = argv[3]
        # De database waarin gezocht moet worden

        mafft(fasta_input, msa_input)

        # Zodat je in de command line niet zo veel input hoeft te geven,
        # wordt er door het script zelf output bestanden gemaakt.
        hmmbuild_output = msa_input.split(".")[0] + ".hmm"
        hmmsearch_output_alignment = hmmsearch_output_file + ".hmmsearch_alignment"
        hmmsearch_output_summary = hmmsearch_output_file + ".hmmsearch.summary"

        hmmbuild(msa_input, hmmbuild_output)

        hmmsearch(hmmbuild_output, hmmsearch_output_alignment, hmmsearch_output_summary, database)

        # Mocht je het script willen testen: python3 hmmtools.py globins_test.fa globins_hmmsearch globins45.fa
        # Wanneer het hele script dan is gerunt, heb je dus in totaal de volgende bestanden:
        # - je MSA input
        # - hmm profiel van hmmbuild
        # - hmmsearch alignment bestand
        # - hmmsearch summary bestand
        # (- je database)

    except IndexError:
        print("Incorrect number of command line arguments."
              "\nUsage: python3 hmmtools.py [msa_input] [hmmsearch_output (no extensions)] [database]")


main()
