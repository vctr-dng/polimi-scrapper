import argparse

from os import path

from scrapper import Scrapper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = """Gather informations regarding Politecnico di Milano courses details page
        """
    )

    parser.add_argument('input', help='String of an URL or path to a file containing URLs')
    parser.add_argument('output', help='Path to save the tsv file output')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()
    verbose = args.verbose

    isInputFile = True if path.isfile(args.input) else False

    isOutputDir = True if path.isdir(args.output) else False

    if not isOutputDir and not path.isfile(args.output):
        raise Exception(f'The specified output : {args.output} is not pointing to a directory nor a file')

    scrap = Scrapper()
