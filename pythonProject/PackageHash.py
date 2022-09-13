import csv

from Package import Package

# Contains things having to do with the hash table used for packages
class ChainingHashTable:
    # Time = (O)1
    # Space = (O)1
    def __init__(self):
        self.table = []
        for i in range(10):
            self.table.append([])

    # Time = (O)n
    # Space = (O)1
    def insert(self, item):
        key = int(item.id)
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        itemnotpresent = True

        for keyvalue in bucket_list:
            if keyvalue[0] == key:
                keyvalue[1] = item
                itemnotpresent = False
        if itemnotpresent:
            key_value = [key, item]
            bucket_list.append(key_value)

    # Time = (O)n
    # Space = (O)1
    def search(self, key):
        bucket = key % len(self.table)
        bucket_list = self.table[bucket]

        for keyvalue in bucket_list:
            if keyvalue[0] == key:
                return keyvalue[1]
        return None

    # Time = (O)n
    # Space = (O)1
    def remove(self, key):
        bucket = key % len(self.table)
        bucket_list = self.table[bucket]

        for keyvalue in bucket_list:
            if keyvalue[0] == key:
                bucket_list.remove([keyvalue[0], keyvalue[1]])

    # Time = (O)n
    # # Space = (O)1
    def populatenewpackagetable(self):
        self.table.clear()
        self.__init__()
        for package in Package.getallpackagesstart():
            self.insert(package)

