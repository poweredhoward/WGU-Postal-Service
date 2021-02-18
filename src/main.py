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
    hashed_packages = HashTable()
    for package in list_of_packages:
        if not truck1.add_package(package):
            truck2.add_package(package)
        hashed_packages.add_package(package)
    
    truck1.set_next_stop({'distance': 0, 'address': "4001 South 700 East,"})
    truck2.set_next_stop({'distance': 0, 'address': "4001 South 700 East,"})


    # all_hashed_packages = hashed_packages.get_all_packages()
    # for p in all_hashed_packages:
    #     print(p.id)
    # for i in range(1, 41):
    #     print(hashed_packages.get_package(i).full_address + str(i))
        
    # print(list_of_packages)
    distances = ingest_distance_data()

    while len(truck1.packages) > 0 or len(truck2.packages) > 0:
        # distance_to_drive = abs(truck1.distance_to_next_stop - truck2.distance_to_next_stop)

        distance_to_drive = 0
        if truck1.finished_driving:
            print("t1 done")
            distance_to_drive = truck2.distance_to_next_stop
            drive_truck(truck2, distance_to_drive, list_of_packages, distances)

        elif truck2.finished_driving:
            print("t2 done")
            distance_to_drive = truck1.distance_to_next_stop
            drive_truck(truck1, distance_to_drive, list_of_packages, distances)

        else:
            distance_to_drive = abs(min([truck1.distance_to_next_stop, truck2.distance_to_next_stop]))
            drive_truck(truck1, distance_to_drive, list_of_packages, distances)
            drive_truck(truck2, distance_to_drive, list_of_packages, distances)
        for truck in [truck1, truck2]:
            if truck.distance_to_next_stop == 0 and not truck.finished_driving:
                truck.set_next_stop(get_next_stop(truck, distances))

            # print("distance " + str(distance_to_drive))
            # truck1.set_next_stop(get_next_stop(truck1, distances))
            # truck2.set_next_stop(get_next_stop(truck2, distances))



        # if distance_to_drive > 0:
        #     drive_truck(truck1, distance_to_drive, list_of_packages)
        #                 # for package in packages_not_picked_up:
        #                 #     if not truck1.add_package(package):
        #                 #         break
                
        #                 # truck1.set_next_stop(get_next_stop(truck1, distances))
        #     if(truck2.drive_x_miles(distance_to_drive) == "Arrived"):
        #         # Need to add logic to truck class to offload packages at this address
        #         truck2.offload_packages_at_address()
                
        #         if len(truck2.packages) == 0:
        #             packages_not_picked_up = [ p for p in list_of_packages if p.delivery_status == "at the hub" ]
        #             if len(packages_not_picked_up) == 0:
        #                 truck2.next_stop = ""
        #                 truck2.distance_to_next_stop = 0.0
        #                 truck2.finished_driving = True
                    
        #             elif truck2.next_stop == "4001 South 700 East,":
        #                 for package in packages_not_picked_up:
        #                     if not truck2.add_package(package):
        #                         break
        #                 truck2.set_next_stop(get_next_stop(truck2, distances))
                        
        #             else:
        #                 # Go back to hub and add more packages
        #                 truck2.set_next_stop({
        #                     "distance": distances[truck2.next_stop][0][1],
        #                     "address": "4001 South 700 East,"
        #                 })

        #                 # for package in packages_not_picked_up:
        #                 #     if not truck2.add_package(package):
        #                 #         break
                
        #                 # truck2.set_next_stop(get_next_stop(truck2, distances))
        # else:
        #     truck1.set_next_stop(get_next_stop(truck1, distances))
        #     truck2.set_next_stop(get_next_stop(truck2, distances))


        print("t1 distance " +  str(truck1.miles_driven))
        print("t2 distance " +  str(truck2.miles_driven))
        print("t1 " + str(len(truck1.packages)))
        print("t2 " + str(len(truck2.packages)))



    # s = get_next_stop(truck1, distances)


    


    # print(get_desired_time())
    # print_all_packages(hashed_packages)
    print("hi")

    # They start at WGU (4001 South 700 East)


    # print("hi")


# def advance_trucks(truck1, truck2):
#     if truck1

def drive_truck(truck, distance_to_drive, list_of_packages, distances):
    if(truck.drive_x_miles(distance_to_drive) == "Arrived"):
        # Need to add logic to truck class to offload packages at this address
        truck.offload_packages_at_address()
        if len(truck.packages) == 0:
            packages_not_picked_up = [ p for p in list_of_packages if p.delivery_status == "at the hub" ]
            if len(packages_not_picked_up) == 0:
                truck.next_stop = ""
                truck.distance_to_next_stop = 0.0
                truck.finished_driving = True
                print("Doneeeeeee")
            
            elif truck.next_stop == "4001 South 700 East,":
                for package in packages_not_picked_up:
                    if not truck.add_package(package):
                        break
                truck.set_next_stop(get_next_stop(truck, distances))
                

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
            # truck.set_next_stop(distance, address)
            return {
                "address": address,
                "distance": distance
            }
    print("egg")
    print(truck.packages)
    
    # If truck is empty



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
        return s[1].strip()
    else:
        return s[0].strip()

main()