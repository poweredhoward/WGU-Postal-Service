import csv
from datetime import time

from classes import Package, Truck
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
            



def main():
    truck1 = Truck(1)
    truck2 = Truck(2)
    list_of_packages = ingest_package_data()
    hashed_packages = HashTable()
    for package in list_of_packages:
        if not truck1.add_package(package):
            truck2.add_package(package)
        hashed_packages.add_package(package)

    # all_hashed_packages = hashed_packages.get_all_packages()
    # for p in all_hashed_packages:
    #     print(p.id)
    # for i in range(1, 41):
    #     print(hashed_packages.get_package(i).full_address + str(i))
        
    # print(list_of_packages)
    distances = ingest_distance_data()
    # print(get_desired_time())
    # print_all_packages(hashed_packages)
    print("hi")

    # They start at WGU (4001 South 700 East)


    # print("hi")


# def advance_trucks(truck1, truck2):
#     if truck1


# def get_next_stop(truck):



def get_desired_time():
    valid = False
    selected_time = ""
    while not valid:
        try:
            inputted_time = input("What time would you like to see? (HH:MM)\n")
            hour, min = map(int, inputted_time.split(':'))
            if hour < 8:
                print("Please select a time after 08:00")
            else:
                selected_time = time(hour=hour, minute=min)
                valid = True
        except:
            print("Please input a valid time format")
        
    return selected_time


def print_all_packages(table):
    packages = table.get_all_packages()
    for package in packages:
        if package.delivery_status != 'delivered':
            print("ID: {}   Address: {}   Status: {}".format(package.id, package.full_address, package.delivery_status))
        else:
            print("ID: {}   Address: {}   Status: {} @ {}".format(package.id, package.full_address, package.delivery_status, package.time_delivered))

def print_trucks_mileage(truck1, truck2):
    print("Miles Driven by Trucks:")
    print("ID: {}    Miles: {}".format(truck1.id, truck1.miles_driven))
    print("ID: {}    Miles: {}".format(truck2.id, truck2.miles_driven))


def trim_stop_name(stop_address):
    s = stop_address.split('\n')
    if len(s) > 1:
        return s[1]
    else:
        return s[0]

main()