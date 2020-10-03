import os
from sys import argv


def hmmbuild(msa_input, hmm_output):
    """


    """
    replace_header(msa_input) # dit is trouwens alleen nodig als we een clustal input geven, niet bij een Stockholm input
    if os.path.isfile(hmm_output):  # file bestaat al
        print("File already exists")
    else:
        e = os.system("hmmbuild --amino {} {}".format(hmm_output, msa_input))  # in hmmbuild moet je eerst je output.hmm opgeven en daarna je input bestand
        # ik heb dit getest met een MSA van 4 globines (zie globins4.sto). Het resultaat is te zien in globins4.hmm.
        # ik begrijp niet alles wat er in het bestand staat, maar het is denk ik niet heel belangrijk


def replace_header(msa_input):
    """


    """
    with open(msa_input, "r") as inFile:
        all_lines = inFile.readlines()
    all_lines[0] = all_lines[0].replace(all_lines[0], "CLUSTAL W (1.82) multiple sequence alignment\n")  # net als t-coffe, gaf hmmbuild ook een error dat hij de clustal header niet herkent. Ik heb toen gewoon weer die header van het voorbeeld van t-coffe gepakt, en die wordt dan in het bestand gezet, in plaats van de originele header

    with open(msa_input, "w") as inFile:
        for line in all_lines:
            inFile.write(line)


def main():  # via de command line kun je het aanroepen via: python3 hmmbuild.py
    try:
        msa_input = argv[1]  # het eerste argument [0] is hmmbuild.py, het tweede je input bestand
        hmmbuild_output = argv[2]
        hmmbuild(msa_input, hmmbuild_output)
    except IndexError:
        print("Incorrect number of command line arguments.\nUsage: python3 hmmbuild.py [msa_input] [hmmbuild_output]")

main()
