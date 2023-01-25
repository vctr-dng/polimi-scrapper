import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = 'Polimi Scrapper',
        description = """Gather informations regarding Politecnico di Milano courses details page
        """
    )

    parser.add_argument('input', help='String of an URL or path to a file containing URLs')
    parser.add_argument('output', metavar='O', help='Path to save the tsv file output')

    args = parser.parse_args()
    print(args)