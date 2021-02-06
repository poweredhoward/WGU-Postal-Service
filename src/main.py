import csv
from classes import Package


def ingest_package_data():
    packages = []
    with open("../data/package_data.csv") as file:
        reader = csv.DictReader(file, delimiter=',')
        line = 0
        for r in reader:
            # print(r)
            p = Package(
                r['ID'],
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

def ingest_distance_data():
    packages = {}
    with open("../data/distance_table.csv") as file:
        reader = csv.reader(file, delimiter=',')
        line = 0
        for row in reader:
            print(row)

def main():
    list_of_packages = ingest_package_data()
    print(list_of_packages)
    # ingest_distance_data()


main()