import csv
def load_csv_file(file_path):
    """
    This function returns a CSV iterable
    """
    return csv.reader(file_path)


def countColNumber(file_path):
    """
    This funciton returns the number of columns(columns) in fileName
    """
    with open(file_path, 'r', encoding="ISO-8859-1") as f:
        return len(next(csv.reader(f)))

def countRowNumber(file_path):
    """
    This funciton returns the number of rows in fileName
    """
    with open(file_path, 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f)
        return sum(1 for row in reader)

def getAttrList(file_path):
    """
    This funciton returns the name of attributes in fileName
    Args:
        fileName
    Returns:
        attrlist: list of attributes
    """

    with open(file_path, 'r', encoding="ISO-8859-1") as f:
        attrlist = next(csv.reader(f))
        return attrlist


def getAttrID(file_path, attr):
    """
    This funciton returns the index of selected attribute in fileName
    Args:
        fileName
        attr(string):the name of the attribute
    Returns:
        attrId: Column No. of the attribute
    """

    with open(file_path, 'r', encoding="ISO-8859-1") as f:
        attrlist = next(csv.reader(f))
        try:
            AttrId = attrlist.index(attr)
        except:
            print("Invalid attribute")
            AttrId = -1
        return AttrId
