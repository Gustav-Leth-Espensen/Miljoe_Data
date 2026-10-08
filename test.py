import unittest
import etl



class test_transformer(unittest.TestCase):

    def test_non_inputs(self):
        etl.transform() == ["hej"]
        return