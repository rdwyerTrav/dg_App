
import unittest
import dgSpatialOps

##confirm test set up
def proveTest():
    return True

##TODO needs tests for geoJSON inputs and formats
##current assumptions are 2 polys in same POST JSON

class app_test(unittest.TestCase):

    def testTrue(self):
        self.assertTrue(proveTest)

    def testFalse(self):
        self.assertFalse(not(proveTest))
        
    def setUp(self):
        self.app = dgSpatialOps.app.test_client()
        dgSpatialOps.app.testing = True
        dgSpatialOps.app.config['DEBUG'] = False

    def test_home(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
    
#####################