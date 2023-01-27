import argparse
import multiprocessing
from multiprocessing.pool import ThreadPool as Pool
from os import path

import pandas as pd
from tqdm import tqdm

from scrapper import Scrapper


def scrapURLs(URLs):

    webScrapper = Scrapper()

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
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    verbose = args.verbose

    isInputFile = True if path.isfile(args.input) else False

    isOutputDir = True if path.isdir(args.output) else False

    if not isOutputDir and not path.isfile(args.output):
        raise Exception(
            f"The specified output : {args.output} is not pointing to a directory nor a file"
        )

    URLs = []
    if isInputFile:
        inputFile = open(args.input, "r")
        data = inputFile.read()
        inputFile.close()
        URLs = data.split("\n")
    else:
        URLs.append(args.input)

    if verbose:
        print(f'{len(URLs)} link{"s" if len(URLs) > 1 else ""} will be scrapped')

    print(scrapURLs(URLs))