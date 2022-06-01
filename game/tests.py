from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.


class TestViews(TestCase):
    """
    Testing for game views
    """
    def setUp(self):
        """ Create test login user"""
        username = "jojo"
        pswd = "Trials"
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username=username,
                                                   password=pswd,
                                                   is_superuser=True)
        logged_in = self.client.login(username=username, password=pswd)

        self.assertTrue(logged_in)
