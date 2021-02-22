# Matthew Howard, 001241461

import csv
from datetime import time, timedelta, datetime

from classes import Package, Truck
from hash_table import HashTable

MINUTES_PER_MILE = 3.333

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
            for address in row:
                if address == "DISTANCE BETWEEN HUBS IN MILES":
                    stop_name = trim_stop_name(row["DISTANCE BETWEEN HUBS IN MILES"])
                elif row[address] != '' and row[address] != 0:
                    packages[stop_name].append((trim_stop_name(address), float(row[address])))
                    packages[trim_stop_name(address)].append((stop_name, float(row[address])))
            p = packages[stop_name]
            # packages[stop_name] = sorted(p, key=lambda x: x[1])

        
    return packages
            



def main():
    truck1 = Truck(1)
    truck2 = Truck(2)
    list_of_packages = ingest_package_data()
    distances = ingest_distance_data()

    current_day = datetime.today()
    current_time = time(hour=8, minute=0)
    current_time = datetime.combine(current_day, current_time)

    hashed_packages = HashTable()
    for package in list_of_packages:
        if package.id in [1, 3, 13, 14, 15, 16, 19, 18, 20, 21, 29, 31, 34, 36, 38, 37]:
        # if package.id in [3, 13, 14, 15, 16, 19, 18, 20, 21, 29, 30, 31, 34, 36, 37, 38]:

            truck2.add_package(package, current_time)
        elif package.id not in [6, 9, 25, 28, 32]:
            truck1.add_package(package, current_time)
        hashed_packages.add_package(package)
    
    truck1.set_next_stop({'distance': 0, 'address': "4001 South 700 East,"})
    truck2.set_next_stop({'distance': 0, 'address': "4001 South 700 East,"})



    desired_time = get_desired_time()
    desired_package = get_desired_package()

    picked_up_late_packages = False
    corrected_package_9 = False


    while (not truck1.finished_driving or not truck2.finished_driving) and current_time <= desired_time:
        if not corrected_package_9:
            corrected_package_9 = check_and_correct_package_9(current_time, hashed_packages)

        distance_to_drive = 0
        if truck1.finished_driving:
            distance_to_drive = truck2.distance_to_next_stop
            current_time = current_time + increment_time(distance_to_drive)
            drive_truck(truck2, distance_to_drive, list_of_packages, distances, current_time)

        elif truck2.finished_driving:
            distance_to_drive = truck1.distance_to_next_stop
            current_time = current_time + increment_time(distance_to_drive)
            drive_truck(truck1, distance_to_drive, list_of_packages, distances, current_time)

        else:
            distance_to_drive = abs(min([truck1.distance_to_next_stop, truck2.distance_to_next_stop]))
            current_time = current_time + increment_time(distance_to_drive)
            drive_truck(truck1, distance_to_drive, list_of_packages, distances, current_time)
            drive_truck(truck2, distance_to_drive, list_of_packages, distances, current_time)

        for truck in [truck1, truck2]:
            if truck.distance_to_next_stop == 0 and not truck.finished_driving:
                if not picked_up_late_packages and current_time.hour >= 9:
                    print(current_time)
                    # TODO: Add logic so that if the truck's destination is ever the hub, load it
                    truck.set_next_stop({
                        "distance": distances[truck.next_stop][0][1],
                        "address": "4001 South 700 East,"
                    })
                    picked_up_late_packages = True
                else:
                    truck.set_next_stop(get_next_stop(truck, distances))
        
        # print("t1 distance " +  str(truck1.miles_driven))
        # print("t2 distance " +  str(truck2.miles_driven))
        # print("t1 " + str(len(truck1.packages)))
        # print("t2 " + str(len(truck2.packages)))
        # print(current_time.strftime("%H:%M"))

    if desired_package == "All":
        all_packages = hashed_packages.get_all_packages()
        packages_to_display = [ p for p in all_packages if p.delivery_status == "delivered" and p.time_delivered < desired_time]
        for pack in packages_to_display:
            print_package(pack.id, hashed_packages)
    else:
        print_package(desired_package, hashed_packages)

    print_trucks_mileage(truck1, truck2)



def drive_truck(truck, distance_to_drive, list_of_packages, distances, current_time):
    if(truck.drive_x_miles(distance_to_drive) == "Arrived"):
        # Need to add logic to truck class to offload packages at this address
        truck.offload_packages_at_address(current_time)
        
        if truck.next_stop == "4001 South 700 East,":
            packages_not_picked_up = [ p for p in list_of_packages if p.delivery_status == "at the hub" ]
            for package in packages_not_picked_up:
                if not truck.add_package(package, current_time):
                    break
            truck.set_next_stop(get_next_stop(truck, distances))
        
        if len(truck.packages) == 0:
            packages_not_picked_up = [ p for p in list_of_packages if p.delivery_status == "at the hub" ]
            if len(packages_not_picked_up) == 0:
                truck.next_stop = ""
                truck.distance_to_next_stop = 0.0
                truck.finished_driving = True

                

            else:
                # Go back to hub and add more packages
                truck.set_next_stop({
                    "distance": distances[truck.next_stop][0][1],
                    "address": "4001 South 700 East,"
                })
                return "Retr"
            return "Done"
        return 



def get_next_stop(truck, distances):
    sorted_distances_for_address = sorted(distances[truck.next_stop], key=lambda x: x[1])
    # sorted_distances_for_address = distances[truck.next_stop]
    # print(sorted_distances_for_address)

    for address, distance in sorted_distances_for_address:
        if address in truck.addresses and distance > 0:
            # deliver_to_address = True
            # packages_at_address = package_table.get_packages_at_address(address)
            # if len(packages_at_address) > 0:
            #     for package in packages_at_address:
            #         if package.

            # truck.set_next_stop(distance, address)
            return {
                "address": address,
                "distance": distance
            }
    print("egg")
    

def increment_time(miles):
    return timedelta(minutes = miles * MINUTES_PER_MILE)


def get_desired_time():
    valid = False
    attempts = 0
    selected_time = ""
    current_day = datetime.today()
    
    while not valid and attempts < 3:
        try:
            attempts += 1
            inputted_time = input("What time would you like to see? (HH:MM)\n")
            hour, min = map(int, inputted_time.split(':'))
            if hour < 8:
                print("Please select a time after 08:00")
            else:
                selected_time = time(hour=hour, minute=min)
                selected_time = datetime.combine(current_day, selected_time)
                valid = True
        except:
            print("Please input a valid time format")
        
    return selected_time


def get_desired_package():
    valid = False
    attempts = 0

    while not valid and attempts < 3:
        try:
            attempts += 1
            inputted_id = input("What package would you like to see? (Provide its ID, or type 'All')\n")
            if inputted_id == "All":
                return inputted_id
            inputted_id = int(inputted_id)
            if inputted_id > 0 and inputted_id <= 40:
                return inputted_id
        except:
            print("Please input a number between 1 and 40\n")


def print_package(id, table):
    package = table.get_package_by_id(id)
    if package.delivery_status != 'delivered':
        print("ID: {}   Address: {}   Deadline: {}   Weight: {}   Status: {}".format(
            package.id, package.full_address, package.deadline, package.mass, package.delivery_status))
    else:
        print("ID: {}   Address: {}   Deadline: {}   Weight: {}   Status: {} @ {}".format(
            package.id, package.full_address, package.deadline, package.mass,
             package.delivery_status, package.time_delivered.strftime("%H:%M")))


def print_trucks_mileage(truck1, truck2):
    print("Miles Driven by Trucks:")
    print("ID: {}    Miles: {}".format(truck1.id, truck1.miles_driven))
    print("ID: {}    Miles: {}".format(truck2.id, truck2.miles_driven))



def trim_stop_name(stop_address):
    s = stop_address.split('\n')
    if len(s) > 1:
        return s[1].strip()
    else:
        return s[0].strip()

def check_and_correct_package_9(current_time, hashed_packages):
    # 410 S State St., Salt Lake City, UT 84111
    if current_time.hour >= 10 and current_time.minute >= 20:
        p9 = hashed_packages.get_package_by_id(9)
        p9.street_address = "410 S State St"
        p9.city = "Salt Lake City"
        p9.state = "UT"
        p9.zip = "84111"

        return True
    return False


main()