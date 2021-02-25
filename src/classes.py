from datetime import datetime

class Package:
    
    def __init__(self, id, address, city, state, zip, deadline, mass, note):
        self.id = id
        self.street_address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.note = note
        self.delivery_status = "at the hub"
        self.time_delivered = None

    @property
    def full_address(self):
        return "{} {}, {} {}".format(
            self.street_address, self.city, self.state, self.zip)
        


class Truck:
    MILES_PER_MINUTE = 0.3
    
    def __init__(self, id):
        self.id = id
        self.packages = []
        self.miles_driven = 0.0
        self.distance_to_next_stop = 0.0
        self.next_stop = ""
        self.addresses = []
        self.finished_driving = False
    
    def add_package(self, package, current_time):
        if len(self.packages) < 16:
            if package.id not in map(lambda p: p.id, self.packages):
                # print("{} loaded @ {}".format(package.id, current_time))
                self.packages.append(package)
                self.addresses.append(package.street_address)
                package.delivery_status = "en route"
                return True
        return False
        
    # Offfloads packages that are destined for the current address
    def offload_packages_at_address(self, current_time):
        address = self.next_stop
        packages_to_offload = [ p for p in self.packages if p.street_address == address ]
        for package in packages_to_offload:
            package.time_delivered = current_time
            package.delivery_status = "delivered"
            # print("{} delivered on truck {}".format(package.id, self.id))

        self.packages = [ p for p in self.packages if p.street_address != address and p.delivery_status != 'delivered' ]
        self.addresses = [ p.street_address for p in self.packages ]

    
    def drive_x_miles(self, miles):
        self.miles_driven += miles
        self.distance_to_next_stop -= miles
        if self.distance_to_next_stop <= 0:
            return "Arrived"
    
    def set_next_stop(self, args):
        self.distance_to_next_stop = float(args['distance'])
        self.next_stop = args['address']


class Stop:
    def __init__(self, address):
        self.address = address
