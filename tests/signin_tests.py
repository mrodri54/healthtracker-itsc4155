import unittest
from app import app, db, User
from werkzeug.security import generate_password_hash

class TestLogin(unittest.TestCase):

    def setUp(self):
        """ Set up the test client before each test """
        self.app = app.test_client()  # test client
        self.app.application.config['TESTING'] = True

    def test_successful_login(self):
        """ Test login with valid credentials """
        response = self.app.post('/login', data=dict(
            username="testuser2",
            password="testpassword"
        ), follow_redirects=True)


        # Used to debug
        # print("Response status code:", response.status_code) 
        # print("Response location:", response.location)
        # print("Response data:", response.data)
        # print("Response content type:", response.content_type)


        # Checks if the login was successful
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')


    def test_unsuccessful_login_invalid_username(self):
        """ Test login with invalid username """
        response = self.app.post('/login', data=dict(
            username="invaliduser",
            password="testpassword"
        ), follow_redirects=True)

        # Checks if the error message is shown for invalid username
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_unsuccessful_login_invalid_password(self):
        """ Test login with invalid password """
        response = self.app.post('/login', data=dict(
            username="testuser2",
            password="invalidpassword"
        ), follow_redirects=True)

        # Checks if the error message is shown for invalid password
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

if __name__ == '__main__':
    unittest.main()
