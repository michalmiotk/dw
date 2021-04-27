import numpy as np

class Cell():
    def __init__(self, distance, y, x, obstacle):
        self.distance = distance
        self.y = y
        self.x = x
        self.closest_obstacle = None
        self.obstacle = obstacle

    def compute_distance_to_obj(self, obj):
        y_diff = self.y - obj.y
        x_diff = self.x - obj.x
        return np.sqrt(np.power(y_diff,2)+np.power(x_diff, 2))
    
    def compute_distance_to_obstacle(self, obj):
        if obj.obstacle:
            return self.compute_distance_to_obj(obj)
        if obj.closest_obstacle:
            return self.compute_distance_to_obj(obj.closest_obstacle)

        return None
    
    def __str__(self):
        return str(self.y)+ "_"+str(self.x)