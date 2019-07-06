
import unittest

from string_shortening_package.string_shortener import StringShortener

class TestStringShortener(unittest.TestCase):

    def test_empty_string(self):
        shortened_string = StringShortener.Instance().shorten("")
        self.assertEqual(shortened_string, "")
    
    def test_invalid_string(self):
        try:
            shortened_string = StringShortener.Instance().shorten("zabce")
        except Exception as ex:
            self.assertEqual(str(ex), 'string is not valid')  
            
    def test_valid_input(self):
        inputs = ["aba",
                  "aa",
                  "cab",
                  "bcab",
                  "bbbbbb",
                  "bbbbbba"]
        
        excepted_output = ["b",
                           "aa",
                           "bb",
                           "b",
                           "bbbbbb",
                           "a"]
        
        outputs = list(map(StringShortener.Instance().shorten, inputs))
        
        self.assertEqual(outputs, excepted_output)

if __name__ == '__main__':
    unittest.main()