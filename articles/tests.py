'''
Created on Mar 28, 2012

@author: Tarjei
'''

import unittest

class BaseTest(unittest.TestCase):
    """ Test the basics! """
    
    def test_add(self):
        self.assertEqual(1, 1, "lol!")
        
    def test_div(self):
        self.assertEqual(3/3, 1, "Deling skal funke!")
        
    def test_errors(self):
        self.assertRaises(1/0, 0, "Skal ikke funke!") 