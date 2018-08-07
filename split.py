import csv

def my_seperater(split_limit, origin_file):
    #split_limit = 3000
    #filehandler = 'oscars.csv'
    #ct = my_seperater(split_limit, filehandler)

    current_limit = split_limit
    with open(origin_file, 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f)
        header = next(reader)
        split_index = 0
        count_file = 0
        split_file_name = origin_file.split('.')[0] + '_split_' + str(split_index) + '.csv'
        with open(split_file_name, 'w') as fs:
            writer_file = csv.writer(fs)
            writer_file.writerow(header)
            count_file += 1
        row_num = 0
        for i, row in enumerate(reader):
            with open(split_file_name, 'a') as fs:
                writer_file = csv.writer(fs)
                writer_file.writerow(row)
            if i > (current_limit - 2):
                current_limit += split_limit
                split_index += 1
                split_file_name = origin_file.split('.')[0] + '_split_' + str(split_index) + '.csv'
                with open(split_file_name, 'w') as fs:
                    writer_file = csv.writer(fs)
                    writer_file.writerow(header)
                    count_file += 1
            row_num += 1
    return count_file
