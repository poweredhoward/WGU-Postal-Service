# Matthew Howard, 001241461

import csv
from datetime import time, timedelta, datetime

from classes import Package, Truck
from hash_table import HashTable

MINUTES_PER_MILE = 3.333

# Create a list of all the packages
def ingest_package_data():
    packages = []
    with open("../data/package_data.csv") as file:
        reader = csv.DictReader(file, delimiter=',')
        line = 0
        for r in reader:
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


# Create a data structure of all the distances between stops
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
    
    # Add packages to satisfy deadline and special notes requirements
    for package in list_of_packages:
        if package.id in [1, 3, 13, 14, 15, 16, 19, 18, 20, 21, 29, 31, 34, 36, 38, 37]:
            truck2.add_package(package, current_time)
        elif package.id not in [6, 9, 25, 28, 32]:
            truck1.add_package(package, current_time)
        hashed_packages.add_package(package)
    
    truck1.set_next_stop({'distance': 0, 'address': "4001 South 700 East,"})
    truck2.set_next_stop({'distance': 0, 'address': "4001 South 700 East,"})

    # Get user input
    desired_time = get_desired_time()
    desired_package = get_desired_package()

    # Late packages are ones that are delayed on flight
    picked_up_late_packages = False
    # Package 9 needs to be corrected eventually
    corrected_package_9 = False

    while (not truck1.finished_driving or not truck2.finished_driving) and current_time <= desired_time:
        if not corrected_package_9:
            corrected_package_9 = check_and_correct_package_9(current_time, hashed_packages)

        if truck1.finished_driving:
            distance_to_drive = truck2.distance_to_next_stop
            current_time = current_time + increment_time(distance_to_drive)
            drive_truck(truck2, distance_to_drive, list_of_packages, distances, current_time)

        elif truck2.finished_driving:
            distance_to_drive = truck1.distance_to_next_stop
            current_time = current_time + increment_time(distance_to_drive)
            drive_truck(truck1, distance_to_drive, list_of_packages, distances, current_time)

        # Drive trucks a distance so that at least one of them reaches its stop
        else:
            distance_to_drive = abs(min([truck1.distance_to_next_stop, truck2.distance_to_next_stop]))
            current_time = current_time + increment_time(distance_to_drive)
            drive_truck(truck1, distance_to_drive, list_of_packages, distances, current_time)
            drive_truck(truck2, distance_to_drive, list_of_packages, distances, current_time)

        for truck in [truck1, truck2]:
            if truck.distance_to_next_stop == 0 and not truck.finished_driving:
                if not picked_up_late_packages and current_time.hour >= 9:
                    # If after 9:00, go back to the hub and pick up the delayed packages
                    truck.set_next_stop({
                        "distance": distances[truck.next_stop][0][1],
                        "address": "4001 South 700 East,"
                    })
                    picked_up_late_packages = True
                else:
                    truck.set_next_stop(get_next_stop(truck, distances))


    if desired_package == "All":
        all_packages = hashed_packages.get_all_packages()
        for pack in all_packages:
            print_package(pack.id, hashed_packages)
    else:
        print_package(desired_package, hashed_packages)

    print_trucks_mileage(truck1, truck2)
    print("Most recent delivery: {}".format(current_time.strftime("%H:%M")))



def drive_truck(truck, distance_to_drive, list_of_packages, distances, current_time):
    # Drive truck specified number of miles
    if(truck.drive_x_miles(distance_to_drive) == "Arrived"):
        truck.offload_packages_at_address(current_time)
        
        # If truck arrived back at the hub, pick up some packages to fill the truck
        if truck.next_stop == "4001 South 700 East,":
            packages_not_picked_up = [ p for p in list_of_packages if p.delivery_status == "at the hub" ]
            for package in packages_not_picked_up:
                if not truck.add_package(package, current_time):
                    break
            truck.set_next_stop(get_next_stop(truck, distances))
        
        if len(truck.packages) == 0:
            packages_not_picked_up = [ p for p in list_of_packages if p.delivery_status == "at the hub" ]
            # Truck is finished driving
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

# Finds the nearest available stop to the current stop
def get_next_stop(truck, distances):
    sorted_distances_for_address = sorted(distances[truck.next_stop], key=lambda x: x[1])

    for address, distance in sorted_distances_for_address:
        if address in truck.addresses and distance > 0:
            return {
                "address": address,
                "distance": distance
            }
    

def increment_time(miles):
    return timedelta(minutes = miles * MINUTES_PER_MILE)


def get_desired_time():
    valid = False
    attempts = 0
    selected_time = ""
    current_day = datetime.today()
    
    while not valid and attempts < 2:
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

    while not valid and attempts < 2:
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
    # Correct address is 410 S State St., Salt Lake City, UT 84111
    if current_time.hour >= 10 and current_time.minute >= 20:
        p9 = hashed_packages.get_package_by_id(9)
        p9.street_address = "410 S State St"
        p9.city = "Salt Lake City"
        p9.state = "UT"
        p9.zip = "84111"

        return True
    return False


main()