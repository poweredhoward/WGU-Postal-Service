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

        self.full_address = "{} {}, {} {}".format(
            self.street_address, self.city, self.state, self.zip)
        
        self.delivery_status = "at the hub"
        self.time_delivered = ""
    
    def update_delivery_status(self, status):
        self.delivery_status = status
    
    def update_time_delivered(self, time):
        self.time_delivered = time



class Truck:
    
    def __init__(self, id):
        self.id = id
        self.packages = []
        self.miles_driven = 0
        self.distance_to_next_stop = 0
        self.next_stop = ""
        self.addresses = []
    
    def add_package(self, package):
        if len(self.packages) < 16:
            if package.id not in map(lambda p: p.id, self.packages):
                self.packages.append(package)
                self.addresses.append(package.street_address)
                return True
        return False
        
    
    def offload_package(self, id):
        self.packages = [ p for p in self.packages if p.id != id]
        self.addresses = [ p.address for p in self.packages if p.id != id]
    
    def drive_one_minute(self):
        self.miles_driven += 0.3
        self.distance_to_next_stop -= 0.3
        if self.distance_to_next_stop <= 0:
            return "Arrived"
    
    def set_next_stop(self, distance, stop_address):
        self.distance_to_next_stop = distance
        self.next_stop = stop_address


class Stop:
    def __init__(self, address):
        self.address = address
