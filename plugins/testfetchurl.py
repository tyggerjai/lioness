import unittest
from database import DataBase
from fetchurl import fetchurl

class testfetchurl(unittest.TestCase):  
                
        def test_get(self):
                #f = fetchurl('')
                f.command("http://google.com")
