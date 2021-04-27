import unittest
from unittest import TestCase
from brushfire import BrushFire
import numpy as np
from cell import  Cell

class Test(TestCase):
    def test_objexists(self):
        b = BrushFire()
        b.in_img = np.array([[0,0,0],
                          [0,0,0],
                          [0,0,0]])
        b._init_sort()
        some_obj = b.get_object_from_open(y=0, x=0)   
        self.assertIsNotNone(some_obj)
    
    def test_objcoors(self):
        b = BrushFire()
        b.in_img = np.array([[0,0,0],
                          [0,0,0],
                          [0,0,0]])
        b._init_sort()
        some_obj = b.get_object_from_open(y=0, x=0)   
        self.assertEqual(some_obj.y, 0)
        self.assertEqual(some_obj.x, 0)

    def test_sort(self):
        b = BrushFire()
        cell = Cell(0, 1,1,False)
        coors = b.get_adjacent_coors(cell)
        self.assertIn([0,0], coors)
        self.assertIn([0,1], coors)
        self.assertIn([0,2], coors)
        self.assertIn([1,0], coors)
        self.assertNotIn([1,1], coors)
        self.assertIn([1,2], coors)
        self.assertIn([2,0], coors)
        self.assertIn([2,1], coors)
        self.assertIn([2,2], coors)

    def test_run(self):
        b = BrushFire()
        b.in_img = np.array([[1,1,1],
                          [0,0,0],
                          [0,0,0]])
        b._init_sort()
        open_list = [str(obj) for obj in b.open]
        self.assertIn("1_0", open_list)
        self.assertIn("1_1", open_list)
        self.assertIn("1_2", open_list)
        self.assertIn("2_0", open_list)
        self.assertIn("2_1", open_list)
        self.assertIn("2_2", open_list)
        close_list = [str(obj) for obj in b.close]
        self.assertIn("0_0", close_list)
        self.assertIn("0_1", close_list)
        self.assertIn("0_2", close_list)

    def test_obstacle(self):
        b = BrushFire()
        b.in_img = np.array([[1,1,1,1],
                             [1,1,1,1],
                             [1,1,1,1],
                             [0,0,0,0]])
        b._init_sort()
        #b.computeStep()
        obstacle_list = [int(obj.obstacle) for obj in b.open]
        self.assertNotIn(0, obstacle_list)

    def test_three_compute_step(self):
        b = BrushFire()
        b.in_img = np.array([[1,1,1,1],
                             [1,1,1,1],
                             [1,1,1,1],
                             [0,0,0,0]])
        b._init_sort()
        b.computeStep()
        #b.computeStep()
        open_list = [str(obj) for obj in b.open]
        open_list = [str(obj) for obj in b.open]
        self.assertIn("3_1", open_list)
        self.assertIn("3_2", open_list)
        self.assertIn("3_3", open_list)

if __name__ == "__main__":
    unittest.main()