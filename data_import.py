import csv

# creating a function to open, read, to save a csv-file into a list of dictionaries
def get_data(filename):
    result = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            result.append(row)
    return(result)

    # hier noch die exception einfügen