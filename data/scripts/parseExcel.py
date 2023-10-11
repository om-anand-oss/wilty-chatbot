import pandas as pd
import numpy as np


def optionalParameters():
  return ["This is My Guest", "Possession", "Unseen bits"]


def addToDictIfExists(df, idx, parameterName, dataDict):
  if df[parameterName][idx]:
    dataDict[parameterName] = df[parameterName][idx]
  return dataDict


def AddOptionalParameters(df, idx, dataDict, parameterList):
  for parameterName in parameterList:
    if df[parameterName][idx]:
      dataDict[parameterName] = df[parameterName][idx]
  return dataDict


def getDataDict():
  df = pd.read_excel("data/wiltyData.xlsx")

  df = df.fillna("")

  data = []
  for idx in df.index:
    newPrompt = {
        "participant": df["Participant"][idx],
        "isItTrue": df["IsItReal"][idx],
        "series": df["Series"][idx],
        "episode": df["Episode"][idx],
        "roundType": df["Round Type"][idx],
        "prompt": df["Prompt"][idx],
        "teamCaptain": df["Team Captain"][idx],
        "promptId": df["Prompt ID"][idx]
    }

    newPrompt = AddOptionalParameters(df, idx, newPrompt, optionalParameters())

    # print(newPrompt)
    data.append(newPrompt)
    # print(participant, isItReal, len(data[participant][isItReal]))
  # print(len(data))
  return data
