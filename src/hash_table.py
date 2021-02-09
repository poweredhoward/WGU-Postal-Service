
class HashTable:
    HASH_SIZE = 60
    def __init__(self):
        self.table = []
        for i in range(0, self.HASH_SIZE):
            self.table.append([])

    

    def get_package(self, id):
        hash_value = self.__hash(id)
        bucket = self.table[hash_value]
        if len(bucket) == 0:
            return None
        for package in bucket:
            if package.id == id:
                return package
    

    def add_package(self, package):
        hash_value = self.__hash(package.id)
        # Prevent duplicates
        for p in self.table[hash_value]:
            if p.id == package.id:
                return
        self.table[hash_value].append(package)
    
    def get_all_packages(self):
        all_packages = []
        for bucket in self.table:
            for package in bucket:
                all_packages.append(package)

        return sorted(all_packages, key=lambda package: package.id) 
    

    def __hash(self, id):
        return (id * 91) % self.HASH_SIZE
