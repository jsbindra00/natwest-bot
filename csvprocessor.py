import pandas as pd
import numpy as np
from docutil import DocUtil
from enum import IntEnum
import re
import datetime


class ExpenditureColumn(IntEnum):
    Date = 0
    Type = 1
    Description = 2
    Value = 3
    Balance = 4
    AccountName = 5
    AccountNumber = 6

arrivalsFolderLocation = r"D:\FILES\Desktop\other\Expenditure analysis\Analysis\2022\arrivals"


def GetExpenditures(predicate, expendituresMatrix):
    lst = []
    for row in expendituresMatrix:
        if predicate(row):
            lst.append(row)
    return np.array(lst)


def UniformDateRegexReplacer(dateStr):
    # replace all 2 digit dates with 4 digits
    match = dateStr.group()
    return match if len(match) == 4 else "20" + match



dateMapping = {"jan" : "01", "feb" : "02", "mar" : "03", "apr" : "04", "may" : "05", "jun" : "06", "jul" : "07", "aug" : "08", "sep" : "09", "oct" : "10", "nov" : "11", "dec" : "12"}

def CleanDate(dateStr):
    dateStr = re.sub("-", "/", dateStr.lower())
    # 01/jan/2022 -> 01/01/2022
    dateStr = re.sub('[a-z]{3}', lambda x: dateMapping[x.group()], dateStr)
    # 01/01/22 -> 01/01/2022
    dateStr = re.sub("(?![0-9]*\/).+", UniformDateRegexReplacer, dateStr)
    return dateStr


def StackCSVs():
    csvFiles = [file for file in DocUtil.ListAllFiles(arrivalsFolderLocation) if DocUtil.GetExtension(file) == ".csv"]
    tempMaster = None
    for file in csvFiles:
        expenditures = pd.read_csv(file, sep=',', header=None,keep_default_na=False, index_col=False).to_numpy()
        tempMaster = np.vstack([tempMaster, expenditures]) if tempMaster is not None else expenditures
    return tempMaster
def CleanMatrix(tempMaster):
    i = 0
    while i < tempMaster.shape[0]:
        row = tempMaster[i]
        try:
            float(str(row[ExpenditureColumn.Value]))
            row[ExpenditureColumn.Date] = CleanDate(row[ExpenditureColumn.Date])
            i += 1
        except(Exception):
            tempMaster = np.delete(tempMaster, i, 0)
            i = i - 1 if i > 0 else 0
    
            
    return tempMaster
def SortMatrix(tempMaster):
    return np.array(sorted(list(tempMaster), key=lambda row: datetime.datetime.strptime(row[0], '%d/%m/%Y')))


def ProcessArrivalsFolder():

    tempMaster = StackCSVs()
    tempMaster = CleanMatrix(tempMaster)
    tempMaster = SortMatrix(tempMaster)
    
    pd.DataFrame(tempMaster).to_csv("processedarrivals.csv", index=False, header=False)


    return tempMaster

    



def GetAllFoodCosts(row):
    return 1

monthlyExpenditures = ProcessArrivalsFolder()