import unittest
from app import app

class TestProfileUpdate(unittest.TestCase):

    def setUp(self):
        """ Set up the test client before each test """
        self.app = app.test_client()  # test client
        self.app.application.config['TESTING'] = True

        self.app.post('/login', data=dict(
            username="testuser2",
            password="testpassword"
        ))

    def test_successful_profile_update(self):
        """ Test successful profile update (username and password) """
        response = self.app.post('/profile', data=dict(
            username="testuser2updated",
            password="testpassword1"
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertIn(b'Profile updated successfully', response.data)
        

if __name__ == '__main__':
    unittest.main()