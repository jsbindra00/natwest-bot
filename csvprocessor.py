import pandas as pd
import numpy as np
from docutil import DocUtil
from enum import IntEnum


class ExpenditureColumn(IntEnum):
    Date = 0
    Type = 1
    Description = 2
    Value = 3
    Balance = 4
    AccountName = 5
    AccountNumber = 6

arrivalsFolderLocation = r"D:\FILES\Desktop\other\Expenditure analysis\Analysis\2022\arrivals"


def ProcessArrivalsFolder():
    csvFiles = [file for file in DocUtil.ListAllFiles(arrivalsFolderLocation) if DocUtil.GetExtension(file) == ".csv"]
    tempMaster = None
    for file in csvFiles:
        print(file)
        expenditures = pd.read_csv(file, sep=',', header=None,keep_default_na=False, index_col=False).to_numpy()
        tempMaster = np.vstack([tempMaster, expenditures]) if tempMaster is not None else expenditures

    print(tempMaster)


    i = 0
    while i < tempMaster.shape[0]:
        row = tempMaster[i]
        try:
            float(str(row[ExpenditureColumn.Value]))
            i += 1
        except(Exception):
            print(row)
            tempMaster = np.delete(tempMaster, i, 0)
            i = i - 1 if i > 0 else 0
    pd.DataFrame(tempMaster).to_csv("foo.csv", index=False, header=False)

    



ProcessArrivalsFolder()