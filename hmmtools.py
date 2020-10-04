import os
from sys import argv


def hmmbuild(msa_input, hmmbuild_output):
    """ function that creates a hmm profile from a multiple sequence alignment
    input: msa_input - a file containing a multiple sequence alignment
           hmmbuild_output - name of file where hmm profile should be written to

    output: -
    """
    replace_header(msa_input)  # alleen nodig als de input clustal format is. Als de eerste iteratie is geweest, hoeft deze functie niet meer te worden aangeroepen denk ik

    if os.path.isfile(hmmbuild_output):  # file bestaat al
        print("hmm file already exists")
    else:
        e = os.system("hmmbuild --amino {} {}".format(hmmbuild_output, msa_input))
        print("hmmbuild was successful")


def replace_header(msa_input):
    """ function that replaces the original file header, with a compatible header
    input: msa_input - a file containing a multiple sequence alignment

    output: -
    """
    with open(msa_input, "r") as inFile:
        all_lines = inFile.readlines()
    # net als t-coffe, gaf hmmbuild ook een error dat hij de clustal header niet herkent. Ik heb toen gewoon weer die
    # header van het voorbeeld van t-coffe gepakt, en die wordt dan in het bestand gezet, in plaats van de originele header
    all_lines[0] = all_lines[0].replace(all_lines[0], "CLUSTAL W (1.82) multiple sequence alignment\n")

    with open(msa_input, "w") as inFile:
        # het bestand wordt overschreven met de vervangende header. Dit kost dus wel wat tijd bij grotere bestanden,
        # maar na de eerste iteratie hoeft dit niet meer te worden gedaan, omdat de resultaten dan wel een goede header
        # hebben (kun je misschien reguleren met een boolean, maar je kunt misschien ook de header in het bestand
        # handmatig één keer aanpassen en dan deze hele functie gewoon weghalen)
        for line in all_lines:
            inFile.write(line)


def hmmsearch(hmm_input, hmmsearch_output_alignment, hmmsearch_output_summary, database):
    """ function that searches a database with a hmm profile
    input: hmm_input - a file containing a hmm profile
           hmmsearch_output_alignment - a file where the MSA of the results should be written to
           hmmsearch_output_summary - a file where the results of the database search should be written to
           database - a file that functions as the database that will be searched against with the hmm profile

    output: -
    """
    if os.path.isfile(hmm_input):  # het hmm profiel bestaat, hmmsearch kan worden uitgevoerd
        if os.path.isfile(hmmsearch_output_alignment) or os.path.isfile(hmmsearch_output_summary):  # de output bestanden bestaan al
            print("hmmsearch result files already exist")
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
        print("Could not find hmm profile, hmmbuild failed")


def main():
    try:
        msa_input = argv[1]  # de MSA input
        hmmsearch_output_file = argv[2]  # een naam voor de hmmsearch output bestanden (zonder extensie)
        database = argv[3]  # database waarin gezocht moet worden

        # zodat je in de command line niet zo veel input hoeft te geven, wordt er door het script zelf output bestanden gemaakt
        hmmbuild_output = msa_input.split(".")[0] + msa_input.split(".")[1].replace(msa_input.split(".")[1], ".hmm")  # dit lijkt heel ingewikkeld, maar in werkelijkeheid vervang ik gewoon de exstensie van het MSA bestand met .hmm
        hmmbuild(msa_input, hmmbuild_output)

        hmmsearch_output_alignment = hmmsearch_output_file + ".hmmsearch_alignment"  # ook hier worden automatisch output bestanden gemaakt
        hmmsearch_output_summary = hmmsearch_output_file + ".hmmsearch.summary"
        hmmsearch(hmmbuild_output, hmmsearch_output_alignment, hmmsearch_output_summary, database)

        # mocht je het script willen testen: python3 hmmtools.py globins_test.fa globins_hmmsearch globins45.fa
        # wanneer het hele script dan is gerunt, heb je dus in totaal de volgende bestanden:
        # - je MSA input
        # - hmm profiel van hmmbuild
        # - hmmsearch alignment bestand
        # - hmmsearch summary bestand
        # (- je database)

    except IndexError:
        print("Incorrect number of command line arguments.\nUsage: python3 hmmtools.py [msa_input] [hmmsearch_output (no extensions)] [database]")


main()
