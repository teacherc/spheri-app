import unittest
import main

class TestMain(unittest.TestCase):
#Test validate_zipcode
    def test_validate_zipcode(self):
        result = main.validate_zipcode("98023")
        self.assertTrue(result, True)
    
    def test_validate_zipcode(self):
        result = main.validate_zipcode("cat")
        self.assertFalse(result, False)
    
    def test_validate_zipcode(self):
        result = main.validate_zipcode("")
        self.assertFalse(result, False)

#Test weather_from
    def test_weather_from(self):
        result = main.weather_from("98023")
        self.assertIn('weather', result.keys())
    
    def test_weather_from(self):
        result = main.weather_from("98023")
        self.assertIn('api_code', result.keys())

#Test authorization_spotify
    def test_authorization_spotify(self):
        token = main.authorization_spotify()
        self.assertTrue(token, True)
    
        
if __name__ == '__main__':
    unittest.main()