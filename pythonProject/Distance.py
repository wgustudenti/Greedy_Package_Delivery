import csv
from decimal import Decimal

import Package


# Returns a table of all distances from one address to another.
# Time = (O)n2
# # Space = (O)n
def getalldistances():
    alldistances = []

    with open("WGUPS Distance Table.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            if "." in row[2]:
                distancesrows = []
                for cell in row:
                    if "." in cell:
                        distancesrows.append(cell)
                alldistances.append(distancesrows)
    return alldistances


# Returns a list of key/value pairs for all addresses.
# Time = (O)n2
# Space = (O)n
def getaddresskeyvaluelist():
    i = 0
    addresskeyvaluelist = []
    with open("WGUPS Distance Table.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            if "DISTANCE" in row[0]:
                cellcount = 0
                for cell in row:
                    seconddimension = []
                    if cellcount > 1 and cellcount < len(row):
                        seconddimension.append(i)
                        seconddimension.append(cell)
                        addresskeyvaluelist.append(seconddimension)
                        i = i + 1
                    cellcount = cellcount + 1
    return addresskeyvaluelist

# Contains things having to do with the distances between addresses
class Distance:
    alldistances = getalldistances()
    addresskeyvaluelist = getaddresskeyvaluelist()

    # Returns the row/column number associated with the address in the alldistances table.
    # Uses a package parameter.
    # Time = (O)n
    # Space = (O)n
    @staticmethod
    def getaddresskeybypackage(package):
        for item in Distance.addresskeyvaluelist:
            if package.address in item[1]:
                return item[0]

    # Returns the row/column number associated with the address in the alldistances table.
    # Uses an address parameter.
    # Time = (O)n
    # Space = (O)n
    @staticmethod
    def getaddresskeybyaddress(address):
        for item in Distance.addresskeyvaluelist:
            if address in item[1]:
                return item[0]

    # Returns the distance between the delivery addresses associated with two different packages.
    # Time = (O)n
    # Space = (O)n
    @staticmethod
    def getdistancebetweenbypackage(package1, package2):
        value1 = Distance.getaddresskeybypackage(package1)
        value2 = Distance.getaddresskeybypackage(package2)
        return Distance.alldistances[value1][value2]

    # Returns the distance between two addresses
    # Time = (O)n
    # Space = (O)n
    @staticmethod
    def getdistancebetweenbyaddress(address1, address2):
        value1 = Distance.getaddresskeybyaddress(address1)
        value2 = Distance.getaddresskeybyaddress(address2)
        return Distance.alldistances[value1][value2]

    # Returns the closest package using an package parameter and a listofpackages parameter.
    # Time = (O)n2
    # Space = (O)n
    @staticmethod
    def getclosestpackagebypackage(package, listofpackages):
        lowestdistance = Distance.getdistancebetweenbypackage(package, listofpackages[0])
        nextpackage = listofpackages[0]
        for item in listofpackages:
            if Decimal(Distance.getdistancebetweenbypackage(package, item)) < Decimal(lowestdistance):
                lowestdistance = Distance.getdistancebetweenbypackage(package, item)
                nextpackage = item
        return nextpackage

    # Returns the closest package using an address parameter and a listofpackaes parameter
    # Time = (O)n2
    # Space = (O)n
    @staticmethod
    def getclosestpackagebyaddress(address, listofpackages):
        lowestdistance = Distance.getdistancebetweenbyaddress(address, listofpackages[0].address)
        nextpackage = listofpackages[0]
        for item in listofpackages:
            if Decimal(Distance.getdistancebetweenbyaddress(address, item.address)) < Decimal(lowestdistance):
                lowestdistance = Distance.getdistancebetweenbyaddress(address, item.address)
                nextpackage = item
        return nextpackage






