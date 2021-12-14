import csv
from pathlib import Path

CSV_FILE = Path('./in_out.csv')
#testdata = list(csv.DictReader(open(CSV_FILE), quoting= csv.QUOTE_NONNUMERIC))
testdata = list(csv.DictReader(open(CSV_FILE)))
print(testdata)


def change_private_to_public(property_name: str) -> str:
    if property_name[0] == 'BC_':
        return property_name[1]
    else:
        return property_name


print( change_private_to_public("_123"))