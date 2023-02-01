import argparse
import multiprocessing
from multiprocessing.pool import ThreadPool as Pool
import os
from os import path

import pandas as pd
from tqdm import tqdm

from scrapper import Scrapper


def scrapURLs(URLs):

    df = pd.DataFrame()

    pool = Pool(multiprocessing.cpu_count() * 2)

    for relevantInformation in tqdm(
        pool.imap_unordered(webScrapper.getRelevantInformation, URLs),
        total=len(URLs),
        colour="green",
    ):
        df = pd.concat([relevantInformation, df], ignore_index=True)

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Gather informations regarding Politecnico di Milano courses details page
        """
    )

    parser.add_argument(
        "input", help="String of an URL or path to a file containing URLs"
    )
    parser.add_argument("output", help="Path to save the tsv file output")
    parser.add_argument("-nd", "--noduplicate", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    input = args.input
    output = args.output
    noduplicate = args.noduplicate
    verbose = args.verbose

    isInputFile = True if path.isfile(input) else False

    isOutputDir = True if path.isdir(output) else False

    if not isOutputDir:

        dir_path = path.split(output)[0]
        if not path.isdir(dir_path):
            try:
                os.makedirs(dir_path)
            except:
                raise Exception(
                    f"The specified output : {output} is to a file path however its parent directory does not exist. The attempt to create the parent failed."
                )

    global webScrapper
    webScrapper = Scrapper()

    URLs = []
    if isInputFile:
        inputFile = open(input, "r")
        data = inputFile.read()
        inputFile.close()
        URLs = data.split("\n")
    else:
        URLs.append(input)

    if verbose:
        print(f'{len(URLs)} link{"s" if len(URLs) > 1 else ""} will be scrapped')

    df = scrapURLs(URLs)

    if verbose:
        print("Scrapping complete. Post-processing the dataframe.")

    df = webScrapper.postProcessDataFrame(df, noduplicate)

    if verbose:
        print("Post-processing done.")
        if noduplicate:
            diff = len(URLs) - len(df)
            print(
                f'Removal of duplicate information was requested : {diff} duplicate{"s" if diff > 0 else "" } were removed.'
            )

    dump = webScrapper.getDump(df)

    if verbose:
        print(f"Here is the result of the scrapping :\n{dump}")

    # Saving dump

    if isOutputDir:
        output = path.join(output, "output.tsv")

    with open(output, "a", newline="\n") as output_file:
        output_file.write(dump)

    print(f"Results are available at {output}")
