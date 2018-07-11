import csv
def load_csv_file(fileName):
    """
    This function return a CSV iterable
    """
    return csv.reader(fileName)
def countColNumber(fileName):
    """
    This funciton return the number of columns(columns) in fileName
    """
    with open(fileName, 'r', encoding="ISO-8859-1") as f:
        return len(next(csv.reader(f)))
def getAttrList(fileName):
    """
    This funciton return the name of attributes in fileName
    Args:
        fileName
    Returns:
        attrlist: list of attributes
    """

    with open(fileName, 'r', encoding="ISO-8859-1") as f:
        attrlist = next(csv.reader(f))
        return attrlist
