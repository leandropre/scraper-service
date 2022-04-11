from config.config import *

response_headers = {'Content-Type': 'application/json'}

post = {"url": "https://www.phaidra.ai"}  
                
class TestPosts(BaseTest):

   
    def test001_post(self):
        """ TestCase-1: Test case for test create post using POST localhost:8080/.*
        **Test Scenario:**
        #. Create post using POST /, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        
        self.lg('#. Create post using POST localhost:8080/, should succeed')
        response = self.post_request_response(uri='/', data=post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in response_headers.keys()]
        [self.assertEqual(response_headers[header], response.headers[header]) for header in response_headers.keys()]    
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(response.json(), {'success': True })        
        
        self.lg('%s ENDED' % self._testID)

    def test002_get(self):
        """ TestCase-2: Test case for test view post using GET localhost:8080/
        **Test Scenario:**
        #. View post using GET localhost:8080/, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
     
        self.lg('#. View post using GET localhost:8080/, should succeed')
        response = self.get_request_response(uri='/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in response_headers.keys()]
        [self.assertEqual(response_headers[header], response.headers[header]) for header in response_headers.keys()]    
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(response.json(), {'success': True }) 
                
        self.lg('%s ENDED' % self._testID)

    