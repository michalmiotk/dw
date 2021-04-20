import cv2
import matplotlib.pyplot as plt
import numpy as np
import operator
#based on https://reader.elsevier.com/reader/sd/pii/S092188901200142X?token=726A9B6EC6684A420233F4D679B328C61DBFD4A6916F416FD54F1870DB950B90637850EBFD75BB188BC5EAFAF9A7AFBD&originRegion=eu-west-1&originCreation=20210420132448
#http://www2.informatik.uni-freiburg.de/~lau/dynamicvoronoi/
class Cell():
    def __init__(self, priority, distance, y, x):
        self.priority = priority
        self.distance = distance
        self.y = y
        self.x = x

    def compute_distance_to_obj(self, obj):
        y_diff = self.y - obj.y
        x_diff = self.x - obj.x
        return np.sqrt(np.pow(y_diff,2)+np.pow(x_diff, 2))

class BrushFire():
    def __init__(self):
        self.img = self.load_img()
        self.obstacle_value = 0
        self.open = []
        self.other = []

    def load_img(self):
        img = cv2.imread("grid.png")
        img = img[:,:,0]
        _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        return img
    
    
    def get_adjacent_coors(self, s: Cell):
        y, x = s.y, s.x
        adjacent_coors = []
        for x_offset in [-1,0,1]:
            for y_offset in [-1,0,1]:
                if y == 0 and x == 0:
                    continue
                adjacent_coors.append([y+y_offset, x+x_offset])
        return adjacent_coors

    def get_object(self, y,x):
        for obj in self.open+self.other:
            if obj.y == y and obj.x == x:
                return obj
        return None

    def lower(self, s):
        for coor in self.get_adjacent_coors(s):
            obj = self.get_object(coor[0], coor[1]):
            if obj:
                distance = s.compute_distance_to_obj(obj)
                if distance< s.distance:
                    s.distance = distance

    def position_to_str(self, y, x):
        return str(y) + "_" + str(x)

    def computeDistanceMap(self):
        print("min max", np.min(self.img), np.max(self.img))
        print(self.img.shape)
        for y in range(self.img.shape[0]):
            for x in range(self.img.shape[1]):
                if self.img[y][x] == self.obstacle_value:
                    self.open.append(Cell(0, 0, y, x))
                else:
                    self.other.append(Cell(np.inf, np.inf, y, x))
        
        while(self.open):
            self.open.sort(key=operator.attrgetter('priority'))
            self.lower(self.open.pop(0))

    def show_img(self):
        plt.imshow( self.img)
        plt.show()
if __name__ == "__main__":
    brushfire = BrushFire()
    brushfire.computeDistanceMap()
    brushfire.show_img()