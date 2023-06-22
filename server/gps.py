import math
import csv
import numpy as np
import bresenham
from scipy.optimize import nnls
import matplotlib.pylab as plt
import sys
import time
from datetime import datetime
#CS21B033

np.set_printoptions(threshold=sys.maxsize)


BLOCK_SIZE = 20
MAX_DIST = 30
"""
    Latitude <=> deltaX
    Longitude <=> deltaY
"""


"""
Given you're looking for a simple formula, this is probably the simplest way to do it, 
assuming that the Earth is a sphere with a circumference of 40075 km.

Length in km of 1° of latitude = always 111.32 km

Length in km of 1° of longitude = 40075 km * cos( latitude ) / 360

https://stackoverflow.com/a/39540339
"""


def delta_position(GPSpos1, GPSpos2):
    latitude1, longitude1 = GPSpos1
    latitude2, longitude2 = GPSpos2

    latitude1, longitude1 = float(latitude1), float(longitude1)
    latitude2, longitude2 = float(latitude2), float(longitude2)

    deltax = (latitude2 - latitude1) * 111.32 * 1000
    deltay = 40075 * 1000 * \
        math.cos((latitude1 + latitude2) / 2) * (longitude2 - longitude1) / 360

    return int(deltax*BLOCK_SIZE/MAX_DIST), int(deltay*BLOCK_SIZE/MAX_DIST)


def gps_from_rel_posn(GPS, deltaX, deltaY):
    lat, long = GPS
    lat2 = deltaX / (111.32*1000) + lat
    long2 = deltaY * 360 / (40075 * 1000 * math.cos((lat + lat2) / 2)) + long
    return lat2, long2


class ReadCSV:
    def __init__(self, recFileName="receiver.csv", transFileName="transmitter.csv"):
        self.recFileName = recFileName
        self.transFileName = transFileName

        self.count = 1

        self.dipolesMapped = False
        self.ABGenerated = False
        self.readFile = False
        self.read_file()

    def read_file(self):
        _recFile = open(self.recFileName)
        _transFile = open(self.transFileName)
        self.recCSV = list(csv.reader(_recFile))
        self.transCSV = list(csv.reader(_transFile))
        readFile = True

    def mapDipoles(self):
        if self.readFile == False:
            self.read_file()
        self.dipoles = []
        i, j = 2, 2
        origin = [self.recCSV[1][0], self.recCSV[1][1]]
        while (i < len(self.recCSV)-1 and j < len(self.transCSV)-1):
            recRelPosn = delta_position(origin, self.recCSV[i][0:2])
            transRelPosn = delta_position(origin, self.transCSV[j][0:2])
            self.dipoles.append([transRelPosn, recRelPosn, self.recCSV[i][3]])
            i = i+1
            j=j+1
            utc_time_i = datetime.strptime(
                self.transCSV[i][2], "%Y-%m-%dT%H:%M:%S.%fZ")
            epoch_time_i = (utc_time_i - datetime(1970, 1, 1)).total_seconds()

            while (j < len(self.transCSV)):
                utc_time_j = datetime.strptime(
                    self.transCSV[j][2], "%Y-%m-%dT%H:%M:%S.%fZ")
                epoch_time_j = (
                    utc_time_j - datetime(1970, 1, 1)).total_seconds()

                utc_time_j1 = datetime.strptime(
                    self.transCSV[j+1][2], "%Y-%m-%dT%H:%M:%S.%fZ")
                epoch_time_j1 = (
                    utc_time_j1 - datetime(1970, 1, 1)).total_seconds()

                if (abs(epoch_time_j1 - epoch_time_i) < abs(epoch_time_j-epoch_time_i)):
                    j += 1
                else:
                    break
        self.dipolesMapped = True

    def generateAB(self):
        if (self.dipolesMapped != True):
            self.mapDipoles()
        # -BLOCK_SIZE to +BLOCK_SIZE
        self.A = np.zeros((len(self.dipoles), (2*BLOCK_SIZE * 2*BLOCK_SIZE)))
        self.B = []
        for idx_d, d in enumerate(self.dipoles):
            path = list(bresenham.bresenham(*d[0], *d[1]))
            for p in path:
                self.A[idx_d][(p[0] + BLOCK_SIZE) * 2 *
                              BLOCK_SIZE + (p[1] + BLOCK_SIZE)] = 1
            self.B.append(-float(d[2]))

        self.ABGenerated = True

    def genMap(self):
        if (self.ABGenerated != True):
            self.generateAB()

        num_variables = self.A.shape[1]
        lambda_reg = 0.01

        PROJ_TKNV = np.concatenate([self.A,
                                    np.sqrt(lambda_reg) * np.eye(num_variables)
                                    ])
        RECV_TKNV = np.concatenate([self.B, np.zeros(num_variables)])

        X, _ = nnls(PROJ_TKNV, RECV_TKNV)
        image = X.reshape(BLOCK_SIZE * 2, BLOCK_SIZE * 2)
        
        plt.figure()
        plt.imshow(image, origin='lower')
        plt.savefig("images/fig"+str(self.count)+".png")
        self.count += 1
        self.ABGenerated = False
        self.dipolesMapped = False
        self.readFile = False
        time.sleep(3)
        self.genMap()


if (__name__ == "__main__"):
    fileParser = ReadCSV()
    fileParser.genMap()
