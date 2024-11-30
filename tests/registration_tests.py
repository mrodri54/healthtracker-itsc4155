import unittest
from app import app  

class TestRegistrationForm(unittest.TestCase):

    def setUp(self):
        """ Set up the test client before each test """
        self.app = app.test_client()  # test client
        self.app.application.config['TESTING'] = True

    def test_successful_registration(self):
        """ Test successful registration """
        response = self.app.post('/signup', data=dict(
            username="Unittestuser",
            first_name="John",
            last_name="Doe",
            email="Unittestuser@example.com",
            password="validpassword123"
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertIn(b'Account created successfully. Please log in.', response.data)


    def test_missing_required_fields(self):
        """ Test missing required fields on registration form """
        response = self.app.post('/signup', data=dict(
            username="",
            first_name="",
            last_name="",
            email="",
            password=""
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
