import csv

def get_entries_in_csv_col(csv_filepath, col_name, delimiter = ','):
    with open(csv_filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = delimiter)
        i_col_requested = 0
        res = []
        for i_row, row in enumerate(csv_reader):
            if i_row == 0:
                for i_col, col in enumerate(row):
                    if col == col_name: i_col_requested = i_col
            else:
                res.append(row[i_col_requested])
        return res
    
