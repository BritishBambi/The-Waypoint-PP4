from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.


class TestViews(TestCase):
    """
    Testing for game views

    Test Case = TC

    TC1 - Test Profile Page
    TC2 - Test Edit Profile Page
    TC3 - Test Delete Profile Page
    """
    def setUp(self):
        """ Create test login user and create Profile entry"""
        username = "jojo"
        pswd = "Trials"
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username=username,
                                                   password=pswd,
                                                   is_superuser=True)
        logged_in = self.client.login(username=username, password=pswd)

        self.assertTrue(logged_in)

    def test_profile_page(self):
        """ TC1 - Test Profile Page view renders correct page """
        response = self.client.get('/profile/jojo')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_edit_profile_page(self):
        """ TC2 - Test edit profile view renders correct page """
        response = self.client.get('/profile/jojo/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/edit_profile.html')

    def test_delete_profile_page(self):
        """ TC3 - Test delete profile view renders correct page """
        response = self.client.get('/profile/jojo/delete')
        user = self.user
        user.delete()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/delete_profile.html')
