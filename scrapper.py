import pandas as pd
import requests
from bs4 import BeautifulSoup


class Scrapper:

    labels = [
        "ID Code",
        "Course Title",
        "Credits (CFU / ECTS)",
        "Name",
        "Track",
        "Semester",
    ]

    renamed_labels = {"Name": "Master", "Credits (CFU / ECTS)": "Credits"}

    sort_order = ["Semester", "Master", "Track", "Credits"]

    sort_direction = [True] * len(sort_order)
    sort_direction[sort_order.index("Semester")] = False
    sort_direction[sort_order.index("Credits")] = False

    def __init__(self):
        pass

    @staticmethod
    def getURLContent(URL: str):
        request = requests.get(URL, stream=True)
        return request.content

    @staticmethod
    def getContentEIC(EIC):
        return " ".join(EIC.get_text().split())

    @staticmethod
    def getRelevantInformation(URL: str) -> pd.DataFrame:

        soup = BeautifulSoup(Scrapper.getURLContent(URL), "html.parser")

        mainSection = soup.find_all("td", class_="CenterBar")[0]

        InfoBoxes = mainSection.find_all("table", class_="BoxInfoCard")

        data = {}

        for infoBox in InfoBoxes:
            labelEIC = infoBox.find_all("td", class_="ElementInfoCard1")
            valueEIC = infoBox.find_all("td", class_="ElementInfoCard2")

            for i in range(len(labelEIC)):
                label = Scrapper.getContentEIC(labelEIC[i])
                value = Scrapper.getContentEIC(valueEIC[i])
                if label == "Credits (CFU / ECTS)":
                    data[label] = float(value)
                else:
                    data[label] = str(value)

        relevantDataFrame = pd.DataFrame(
            {label: data[label] for label in Scrapper.labels}, index=[0]
        )
        relevantDataFrame.insert(relevantDataFrame.shape[1], "URL", URL)

        return relevantDataFrame

    @staticmethod
    def postProcessDataFrame(df: pd.DataFrame, rmDuplicate=False) -> pd.DataFrame:
        """
        Rename some columns
        Remove duplicate entries
        """

        df.rename(columns=Scrapper.renamed_labels, inplace=True)

        if rmDuplicate:
            df = df.drop_duplicates(subset=["ID Code"], keep="first")

        df = df.sort_values(
            by=Scrapper.sort_order, ascending=Scrapper.sort_direction, ignore_index=True
        )

        return df

    def getDump(self, df: pd.DataFrame) -> str:
        dfGroups = df.groupby(["Master", "Track"], sort=False)

        rowGroups = list(dfGroups.groups.keys())

        dump = (
            df.head(0)
            .drop(columns=["Master", "Track"])
            .to_csv(sep="\t", index=False, header=True)
        )

        for i in range(len(rowGroups)):
            group = rowGroups[i]
            masterName = group[0]
            trackName = group[1]
            if masterName != rowGroups[i - 1][0]:
                # print(masterName)
                dump += "\n" + masterName + "\t" * (df.shape[1] - 2 - 1) + "\n"
            # print(f'\t{trackName}')
            dump += "\n\t" + trackName + "\t" * (df.shape[1] - 1 - 2 - 1) + "\n\n"

            truncatedDataFrame = dfGroups.get_group(group).drop(
                columns=["Master", "Track"]
            )
            dump += truncatedDataFrame.to_csv(sep="\t", index=False, header=False)

        return dump
