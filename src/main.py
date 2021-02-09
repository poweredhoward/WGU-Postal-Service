import csv
from classes import Package
from hash_table import HashTable

def ingest_package_data():
    packages = []
    with open("../data/package_data.csv") as file:
        reader = csv.DictReader(file, delimiter=',')
        line = 0
        for r in reader:
            # print(r)
            p = Package(
                int(r['ID']),
                r['Address'],
                r['City'],
                r['State'],
                r['Zip'],
                r['Delivery Deadline'],
                r['Mass'],
                r['Notes']
            )
            
            packages.append(p)
    return packages

def ingest_distance_data1():
    packages = {}
    with open("../data/distance_table.csv") as file:
        reader = csv.reader(file, delimiter=',')
        line = 0
        column_names = []
        for row in reader:
            if line != 0:
                for stop in row:
                    # if len(stop) > 10:
                    #     packages[stop].append()
                    if len(stop) < 10:
                        packages
                    elif stop == '':
                        break
                    elif stop == 0:
                        break
                        # packages[] = row[0]
            else:
                column_names = row
                for col in column_names:
                    packages[col] = []
            line += 1


def ingest_distance_data():
    packages = {}
    with open("../data/distance_table.csv") as file:
        dict_reader = csv.DictReader(file, delimiter=',')
        line = 0
        column_names = dict_reader.fieldnames
        for col in column_names:
            packages[trim_stop_name(col)] = []

        for row in dict_reader:
            stop_name = ""
            for entry in row:
                if entry == "DISTANCE BETWEEN HUBS IN MILES":
                    stop_name = trim_stop_name(row["DISTANCE BETWEEN HUBS IN MILES"])
                elif row[entry] != '' and row[entry] != 0:
                    packages[stop_name].append((trim_stop_name(entry), row[entry]))
                    packages[trim_stop_name(entry)].append((stop_name, row[entry]))
        
    return packages
            

def trim_stop_name(stop_address):
    return stop_address.split('\n')[0]


def main():
    list_of_packages = ingest_package_data()
    hashed_packages = HashTable()
    for package in list_of_packages:
        hashed_packages.add_package(package)
    # all_hashed_packages = hashed_packages.get_all_packages()
    # for p in all_hashed_packages:
    #     print(p.id)
    # for i in range(1, 41):
    #     print(hashed_packages.get_package(i).full_address + str(i))
        
    # print(list_of_packages)
    distances = ingest_distance_data()
    print("hi")


main()