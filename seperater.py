import csv

def my_seperater(split_limit, origin_file):
    """
    This funciton accepts a CSV file and an integer split_limit, split the CSV file into several small CSV files 
    with split_limit as the maximum number of tuples in each CSV file
    Args:
        split_limit: maximum number of tuples in each CSV file
        origin_file: file name of original file
    Returns:
        count_file: an Integer indicates the number of files splitted from origin_file
    """

    current_limit = split_limit
    with open(origin_file, 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f)
        header = next(reader)
        split_index = 0
        count_file = 0
        split_file_name = origin_file.split('.')[0] + '_split_' + str(split_index) + '.csv'
        with open(split_file_name, 'w', encoding="ISO-8859-1") as fs:
            writer_file = csv.writer(fs)
            writer_file.writerow(header)
            count_file += 1
        row_num = 0
        for i, row in enumerate(reader):
            with open(split_file_name, 'a', encoding="ISO-8859-1") as fs:
                writer_file = csv.writer(fs)
                writer_file.writerow(row)
            if i > (current_limit - 2):
                current_limit += split_limit
                split_index += 1
                split_file_name = origin_file.split('.')[0] + '_split_' + str(split_index) + '.csv'
                with open(split_file_name, 'w', encoding="ISO-8859-1") as fs:
                    writer_file = csv.writer(fs)
                    writer_file.writerow(header)
                    count_file += 1
            row_num += 1
    return count_file
