from Bio import Entrez
import time


def get_acc_list():
    """ function that searches Protein database on search term, and retrieves accession codes from each result
    """
    Entrez.email = "NBA.Somsen@student.han.nl"  # always tell NCBI who you are

    print("Retrieving database entries... This may take a while ")
    handle_search_id = Entrez.esearch(db="Protein", term="Actinobacteria[Organism]", idtype="acc", retmax="350000")
    # als je op term=txid1760 zoek (wat de id is in de taxonomy browser), dan krijg je maar 35.412 resultaten
    # maar als je op Actinobacteria[Organism] zoekt, dan krijg je 95 miljoen resultaten

    print("All entries have been retrieved. Currently making accession code list...")
    record = Entrez.read(handle_search_id)  # results are saved in record variable
    acc_list = record["IdList"]
    print("Number of sequences found: " + record["Count"] + "\n")

    get_seqs(acc_list)


def get_seqs(acc_list):
    """ function that fetches sequences from Protein database by accession codes, and writes results to file
    :param acc_list: list containing all accession codes
    """
    database_file = "databaseV2.fasta"

    for i in range(len(acc_list)):
        print("Writing sequence from: " + str(acc_list[i]) + " to file" + " ({})".format(str(i+1) + "/" + str(len(acc_list))))
        handle_fetch = Entrez.efetch(db="Protein", id=acc_list[i], rettype="fasta")
        record = handle_fetch.read()
        with open(database_file, "a") as inFile:
            inFile.write(record.strip() + "\n")  # elk record had 2 new lines op het eind, maar ik wil er maar 1
        time.sleep(0.2)  # to not overload NCBI
    print("\nDatabase acquired")


def main():
    # in database.fasta zitten nu ongeveer 10.000 sequenties, maar het zijn niet echt allemaal verschillende organismen
    get_acc_list()


main()
