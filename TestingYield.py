from collections import namedtuple

class dataPoints(namedtuple):
    x: int
    y: int
    z: int

def file_reader(file):
    for row in file:
        cols = row.rstrip().split(",")
        cols = [float(c) for c in cols]
        yield dataPoints._make(cols)

def example_reader():
    with open("mydata.txt") as file:
        for row in file_reader(file):
            print (row)
