from django.test import TestCase
from django.urls import reverse
#import requests
#from .models import Ingredient

# Create your tests here.

class FetchRecipe(TestCase):
    from unittest.mock import patch
    import requests

    url = reverse("fetch_recipe")
    payload = {"site": "https://www.gimmesomeoven.com/chipotle-chicken/"}
    

    def test_no_site_field_in_request_returns_400(self):
        payload = {}

        response = self.client.get(self.url, payload, format="json") 

        self.assertEqual(response.status_code, 400)
        self.assertEqual("MISSING_SITE_URL", response.json()["code"]) 

    @patch("requests.get") 
    def test_network_connection_fails_returns_502(self, mock_get):
        
        mock_get.side_effect = self.requests.exceptions.ConnectionError("Failed to connect")

        response= self.client.get(self.url, self.payload)

        self.assertEqual(response.status_code, 502) 
        self.assertEqual("CONNECTION_ERROR", response.json()["code"]) 

    def test_timeout_returns_502(self):
        payload = {"site": "https://httpbin.org/delay/11"}
        response= self.client.get(self.url, payload)
        self.assertEqual(response.status_code, 502) 
        self.assertEqual("TIMEOUT", response.json()["code"])
        return ""

    def test_no_site_exists_returns_404(self):
        payload = {"site": "https://httpbin.org/status/404"}
        
        response= self.client.get(self.url, payload)
               
        self.assertEqual(response.status_code, 404) 
        self.assertEqual("SITE_NOT_FOUND", response.json()["code"]) 

    def test_other_connection_erro_returns_502(self):
        payload = {"site": "httpbin.org/status/404"}
        
        response= self.client.get(self.url, payload)
            
        self.assertEqual(response.status_code, 502) 
        self.assertEqual("CONNECTION_ERROR", response.json()["code"]) 

    #def test_no_recipe_exists_returns_422(self):
        #return ""

    #def test_recipe_exists(self):
        #return ""
    

    



    
    