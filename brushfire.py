import cv2
import matplotlib.pyplot as plt
import numpy as np
import operator
from cell import Cell

#based on https://reader.elsevier.com/reader/sd/pii/S092188901200142X?token=726A9B6EC6684A420233F4D679B328C61DBFD4A6916F416FD54F1870DB950B90637850EBFD75BB188BC5EAFAF9A7AFBD&originRegion=eu-west-1&originCreation=20210420132448
#http://www2.informatik.uni-freiburg.de/~lau/dynamicvoronoi/

class BrushFire():
    def __init__(self):
        self.in_img = self.load_img()
        self.out_img = np.zeros((self.in_img.shape))
        self.obstacle_value = 0
        self.open = []
        self.close = []
        self._inf_distance = 100
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
                if y_offset == 0 and x_offset == 0:
                    continue
                adjacent_coors.append([y+y_offset, x+x_offset])
        return adjacent_coors

    def get_object_from_open(self, y,x):
        for i, obj in enumerate(self.open):
            if obj.y == y and obj.x == x:
                return self.open.pop(i)
    
    def get_object_from_close(self, y,x):
        for i, obj in enumerate(self.close):
            if obj.y == y and obj.x == x:
                return self.close.pop(i)
        

    def lower(self, s):
        for coor in self.get_adjacent_coors(s):
            obj = self.get_object_from_open(coor[0], coor[1])
            obj_from_close = False
            if not obj:
                obj = self.get_object_from_close(coor[0], coor[1])
                obj_from_close = True
            if obj:
                
                if obj.obstacle:
                    if obj_from_close:
                        self.close.append(obj)
                    else:
                        self.open.append(obj)
                    continue
                
                distance = obj.compute_distance_to_obstacle(s)
                
                
                if distance and distance< obj.distance:
                    obj.distance = distance
                    print("new distance is ", distance)
                    obj.closest_obstacle = s if s.obstacle else s.closest_obstacle
                    self.open.append(obj)
                else:
                    self.close.append(obj)

        self.close.append(s)

    def position_to_str(self, y, x):
        return str(y) + "_" + str(x)
    
    def _init_sort(self):
        for y in range(self.in_img.shape[0]):
            for x in range(self.in_img.shape[1]):
                if self.in_img[y][x] == self.obstacle_value:
                    self.open.append(Cell(0, y, x, True))
                else:
                    self.close.append(Cell(self._inf_distance, y, x, False))

    def computeStep(self):
        self.open.sort(key=operator.attrgetter('distance'))
        #print(len(self.open), len(self.close), "total", len(self.open) + len(self.close))
        self.lower(self.open.pop(0))

    def computeDistanceMap(self):
        #print("min max", np.min(self.in_img), np.max(self.in_img))
        print(self.in_img.shape)
        self._init_sort()
        
        while(self.open):
            self.computeStep()

    def update_out_img_from_close(self):
        for cell in self.close:
            self.out_img[cell.y][cell.x] = cell.distance

    def show_in_img(self):
        plt.imshow(self.in_img)
        plt.title("in img")
        plt.show()
    
    def show_out_img(self):
        plt.imshow(self.out_img)
        plt.title("out img")
        plt.show()

if __name__ == "__main__":
    brushfire = BrushFire()
    brushfire.computeDistanceMap()
    brushfire.update_out_img_from_close()
    brushfire.show_in_img()
    brushfire.show_out_img()