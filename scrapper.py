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

    def __init__(self):
        pass

    @staticmethod
    def __call__():
        print("called")

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

        relevantData = pd.DataFrame(
            {label: data[label] for label in Scrapper.labels}, index=[0]
        )
        relevantData.insert(relevantData.shape[1], "URL", URL)

        return relevantData
