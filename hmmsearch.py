import os
from sys import argv


def hmmsearch(hmm_input, hmmsearch_output_alignment, hmmsearch_output_summary, database):
    """ function that searches a database with a hmm profile
    input: hmm_input - a file containing a hmm profile
           hmmsearch_output_alignment - a file where the MSA of the results should be written to
           hmmsearch_output_summary - a file where the results of database search should be written to
           database - a file that functions as the database that will be searched against with the hmm profile

   output: -
    """

    if os.path.isfile(hmm_input):  # het hmm profiel bestaat, hmmsearch kan worden uitgevoerd
        # oke we moeten met zijn allen even wat dingen bespreken. Je kunt hmmsearch op meerder manieren gebruiken (zie documentatie http://eddylab.org/software/hmmer/Userguide.pdf)
        # de eerste manier is deze:
        e = os.system("hmmsearch -A {} {} {}".format(hmmsearch_output_alignment, hmm_input, database))
        # Wanneer je -A gebruikt, dan moet je eerst je output file opgeven, dan je hmm-profiel en daarna de database. Dat is alleen wel in Stockholm format, en je kunt dat niet in een ander format verdanderen
        # Met -A sla je de multiple alignment op van alle significante hits die gevonden zijn met hmmsearch.
        # Ik heb dit getest met de volgende bestanden:
        # globins4.sto - een MSA van 4 globine sequenties in Stockholm format (hmm tools werken het best met Stockholm format)
        # globins4.hmm - een hmm profiel van globins4.sto
        # globins45.fa - een bestand dat als database dient, het bevat 45 globine sequenties
        # globins4.hmmsearch_alignment - de resultaten van een hmmsearch, profiel: globins4.hmm, database: globins45.fa

        # het bestand globins4.hmmsearch_alignment bevat dus de resultaten van de code in line 13. Als je dat bestand opent,
        # dan zie je de de multiple alignment van alle significante hits die gevonden zijn met hmmsearch in de database (in dit geval was de database dus globins45.fa).
        # dit is alleen in Stockholm format, en het is mij niet helemaal mee duidelijk wat we hier nou mee moeten. Zijn
        # dit de sequenties de we nu bij de originele (globins4.sto) moeten toevoegen? Of zijn dit nu gewoon onze nieuwe sequenties waarmee we
        # moeten gaan ittereren?

        # de tweede manier:
        e = os.system("hmmsearch {} {} > {}".format(hmm_input, database, hmmsearch_output_summary))
        # Ik heb ook dit getest, met dezelfde bestanden als bij de eerste manier, maar nu is het output bestand:
        # globins4.hmmsearch_summary.
        # bij deze methode krijg je ander output dan bij de eerste methode (zie globins4.hmmsearch_summary).
        # je krijgt voor elke alignment e-value en score enzo te zien, vervolgens komt elke alignment, en helmaal onderaan
        # zie je een kleine summary, met bijvoorbeeld hoeveel resultaten er zijn verkregen.
        # Ik denk zelf dat we de eerste methode moeten gebruiken voor de itteraties, maar ik denk dat het ook handig is
        # om deze methode te gebruiken, zodat je wat meer informatie krijgt over je resultaten (hoeveel resultaten je krijgt bijvoorbeeld)


        # ik heb nog niet echt getest met onze MSA, want ik denk dat we het beste eerst allemaal samen even wat dingen moeten overleggen

    else:
        print("Could not find hmm profile, hmmbuild failed")


def main():
    try:
        hmm_input = argv[1]  # het eerste argument [0] is hmmbuild.py, het tweede je input bestand
        hmmsearch_output_alignment = argv[2]  # file dat de alignment gaat bevatten in Stockholm format
        hmmsearch_output_summary = argv[3]  # file dat de alignment summary gaat opslaan
        database = argv[4]
        hmmsearch(hmm_input, hmmsearch_output_alignment, hmmsearch_output_summary, database)

    except IndexError:
        print("Incorrect number of command line arguments.\nUsage: python3 hmmsearch.py [hmm_input] [hmmsearch_output_alignment] [hmmsearch_output_summary] [database]")


main()
