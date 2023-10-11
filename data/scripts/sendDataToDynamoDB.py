import boto3
from parseExcel import getDataDict, optionalParameters

client = boto3.client("dynamodb")
# print(response)


def filterItemValue(itemValue):
  # print(itemValue, type(itemValue))
  if itemValue is None:
    return ""
  return str(itemValue)


def createDynamoDBItem(prompt):
  Item = {
      "participant": {
          "S": filterItemValue(prompt["participant"]),
      },
      "isItTrue": {
          "S": filterItemValue(prompt["isItTrue"]),
      },
      "series": {
          "N": filterItemValue(prompt["series"]),
      },
      "episode": {
          "N": filterItemValue(prompt["episode"]),
      },
      "roundType": {
          "S": filterItemValue(prompt["roundType"]),
      },
      "prompt": {
          "S": filterItemValue(prompt["prompt"]),
      },
      "teamCaptain": {
          "S": filterItemValue(prompt["teamCaptain"]),
      },
      "promptId": {
          "N": filterItemValue(prompt["promptId"]),
      }
  }

  for parameter in optionalParameters():
    if parameter in prompt:
      Item[parameter] = {"S": filterItemValue(prompt[parameter])}
  return Item


def createPutRequest(prompt):
  putRequest = {
      "PutRequest": {
          "Item": createDynamoDBItem(prompt)
      }
  }
  return putRequest


def createBatchWrite(data, tableName):
  batchWriteRequest = {
      tableName: []
  }

  for prompt in data:
    batchWriteRequest[tableName].append(createPutRequest(prompt=prompt))
  return batchWriteRequest


def sendDataToDB(data, tableName):
  for i in range(0, len(data), 25):
    startIndex = i
    endIndex = min(i+25, len(data))

    response = client.batch_write_item(
        RequestItems=createBatchWrite(
            data[startIndex:endIndex], tableName=tableName),
        ReturnConsumedCapacity='TOTAL',
        ReturnItemCollectionMetrics='SIZE'
    )
    print(response)


sendDataToDB(getDataDict(), "wiltyDB")
