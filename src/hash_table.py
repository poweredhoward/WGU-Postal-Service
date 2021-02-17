
class HashTable:
    HASH_SIZE = 60
    def __init__(self):
        self.table = []
        self.address_to_id_mapping = {}
        for i in range(0, self.HASH_SIZE):
            self.table.append([])

    

    def get_package_by_id(self, id):
        hash_value = self.__hash(id)
        bucket = self.table[hash_value]
        if len(bucket) == 0:
            return None
        for package in bucket:
            if package.id == id:
                return package
    
    def get_packages_at_address(self, street_address):
        packages = []
        ids = self.address_to_id_mapping[street_address]
        for id in ids:
            packages.append(self.get_package_by_id(id))
        return packages
        

    def add_package(self, package):
        hash_value = self.__hash(package.id)
        # Prevent duplicates
        for p in self.table[hash_value]:
            if p.id == package.id:
                return
        self.table[hash_value].append(package)
        if package.street_address not in self.address_to_id_mapping:
            self.address_to_id_mapping[package.street_address] = [package.id]
        else:
            self.address_to_id_mapping[package.street_address].append(package.id)
    
    def get_all_packages(self):
        all_packages = []
        for bucket in self.table:
            if len(bucket) > 0:
                for package in bucket:
                    all_packages.append(package)

        return sorted(all_packages, key=lambda package: package.id)
    

    def __hash(self, id):
        return (id * 91) % self.HASH_SIZE
