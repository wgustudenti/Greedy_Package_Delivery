import csv
from datetime import timedelta

# Contains things having to do with the packages
class Package:
    # Time = (O)1
    # Space = (O)1
    def __init__(self, packageid, address, city, state, zipcode, deadline, weight, special, status, timeavailable):
        self.id = packageid
        self.address = address
        self.deadline = deadline
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.weight = weight
        self.special = special
        self.status = status
        self.timeavailable = timeavailable
        self.deliverytime = "N/A"

    # Time = (O)n
    # Space = (O)n
    @staticmethod
    def getallpackagesstart():
        allpackages = []
        with open('WGUPS Package File.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].isnumeric():
                    if Package.gettimeavailable(row[7]) != timedelta(hours=8):
                        timeavailable = Package.gettimeavailable(row[7])
                    else:
                        timeavailable = timedelta(hours=8)
                    package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], "at the hub", timeavailable)
                    allpackages.append(package)
            return allpackages


    # Returns the hour of a deadline for a package.
    # Time = (O)n
    # Space = (O)n
    def getdeadlinehour(self):
        deadlinehour = ""
        for letter in self.deadline:
            if letter != ":":
                deadlinehour = deadlinehour + letter
            else:
                break
        deadlinehour = int(deadlinehour)
        if "PM" in self.deadline:
            deadlinehour = deadlinehour + 12
        return deadlinehour

    # Returns the minute of a deadline for a package.
    # Time = (O)n
    # Space = (O)n
    def getdeadlineminute(self):
        deadlineminute = ""
        i = 0
        for letter in self.deadline:
            if letter == ":":
                deadlineminute = deadlineminute + self.deadline[i+1] + self.deadline[i+2]
                break
            i = i + 1
        return deadlineminute

    # Returns the hour portion of a string representing a time.  24 hour time.
    # If PM in string, adds 12 hours.
    # Time = (O)n
    # Space = (O)n
    @staticmethod
    def gettimestringhour(timestring):
        deadlinehour = ""
        for letter in timestring:
            if letter != ":":
                deadlinehour = deadlinehour + letter
            else:
                break
        deadlinehour = int(deadlinehour)
        if "PM" in timestring:
            deadlinehour = deadlinehour + 12
        return deadlinehour

    # Returns the minute portion of a string representing a time.
    # Time = (O)n
    # Space = (O)n
    @staticmethod
    def gettimestringminute(timestring):
        deadlineminute = ""
        i = 0
        for letter in timestring:
            if letter == ":":
                deadlineminute = deadlineminute + timestring[i+1] + timestring[i+2]
                break
            i = i + 1
        return deadlineminute

    # Returns a timedelta object from a string
    # Time = (O)n
    # Space = (O)n
    @staticmethod
    def gettimedelta(timestring):
        timetoreturn = timedelta(hours=float(Package.gettimestringhour(timestring)), minutes=float(Package.gettimestringminute(timestring)))
        return timetoreturn

    # Returns the time a package is available from their "special" property
    # Time = (O)n
    # Space = (O)n
    @staticmethod
    def gettimeavailable(specialstring):
        timestring = ""
        pmoffset = timedelta(hours=12)
        for letter in specialstring:
            if letter.isnumeric() or letter == ":":
                timestring = timestring + letter
        if ":" not in timestring:
            timestring = "8:00"
        if "PM" in specialstring:
            timedeltaobject = Package.gettimedelta(timestring) + pmoffset
        else:
            timedeltaobject = Package.gettimedelta(timestring)
        return timedeltaobject




