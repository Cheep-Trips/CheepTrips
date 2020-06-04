from django.test import TestCase
from trips.models import *

# for specifying dates
import datetime
import pytz

# for checking user authentication
from django.contrib import auth

# for testing sending emails
from django.core import mail

# for modifying path during testing
import sys

# for testing button and links
from splinter import Browser
#from chromedriver import binary_path
from selenium.webdriver import Chrome

#Note will have to change from username to email when the user model is fixed
class TestAuthentication(TestCase):

    def setUp(self):
        self.oldUser = User.objects.create_user(username = 'oldAccount', \
                                                email='oldAccount@test.com', \
                                                password='oldPassword1')

    def test_sign_up_new_account(self): 

        self.assertTrue(User.objects.filter(username='newAccount').count() == 0)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

        self.client.post('/accounts/register/', {'username': 'newAccount', \
                                    'email': 'newAccount@test.com', \
                                    'password1': 'newPassword1', \
                                    'password2': 'newPassword1'}, follow=True)  
        
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        newUser = User.objects.filter(username='newAccount')[0]
        self.assertEqual(newUser.username, 'newAccount')
        self.assertEqual(newUser.email, 'newAccount@test.com')
        self.assertTrue(newUser.check_password('newPassword1'))

    def test_sign_up_old_email(self): 

        self.assertTrue(User.objects.filter(username='newAccount').count() == 0)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

        self.client.post('/accounts/register/', {'username': 'newAccount', \
                                    'email': 'oldAccount@test.com', \
                                    'password1': 'newPassword1', \
                                    'password2': 'newPassword1'}, follow=True)  
        
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        newUser = User.objects.filter(username='newAccount')[0]
        self.assertEqual(newUser.username, 'newAccount')
        self.assertEqual(newUser.email, 'oldAccount@test.com')
        self.assertTrue(newUser.check_password('newPassword1'))
        

    def test_sign_up_diff_passwords(self): 

        self.assertTrue(User.objects.filter(username='newAccount').count() == 0)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

        self.client.post('/accounts/register/', {'username': 'newAccount', \
                                    'email': 'newAccount@test.com', \
                                    'password1': 'newPassword1', \
                                    'password2': 'diffPassword1'}, follow=True)  
        
        self.assertTrue(User.objects.filter(username='newAccount').count() == 0)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_sign_up_old_account(self): 

        self.assertTrue(User.objects.filter(username='oldAccount').count() == 1)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

        self.client.post('/accounts/register/', {'username': 'oldAccount', \
                                    'email': 'oldAccount@test.com', \
                                    'password1': 'oldPassword10', \
                                    'password2': 'oldPassword10'}, follow=True)  
        
        self.assertTrue(User.objects.filter(username='oldAccount').count() == 1)
        self.assertFalse(auth.get_user(self.client).is_authenticated)


    def test_sign_up_invalid_email(self): 

        self.assertTrue(User.objects.filter(username='newAccount').count() == 0)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

        self.client.post('/accounts/register/', {'username': 'newAccount', \
                                    'email': 'notAnEmail', \
                                    'password1': 'newPassword1', \
                                    'password2': 'diffPassword1'}, follow=True)  
        
        self.assertTrue(User.objects.filter(username='newAccount').count() == 0)
        self.assertFalse(auth.get_user(self.client).is_authenticated)


    def test_login(self):
        self.assertEqual(User.objects.filter(email="oldAccount@test.com")[0], self.oldUser)

        # test for wrong username
        self.client.post('/accounts/login/', {'username': 'newAccount', \
                                    'password': 'oldPassword1'}, follow=True)      
        self.assertFalse(auth.get_user(self.client).is_authenticated)

        # test for wrong password
        self.client.post('/accounts/login/', {'username': 'oldAccount', \
                                    'password': 'diffPassword'})      
        self.assertFalse(auth.get_user(self.client).is_authenticated)

        # test for correct email and password
        self.client.post('/accounts/login/', {'username': 'oldAccount', \
                                        'password': 'oldPassword1'}, follow=True)      
        self.assertTrue(auth.get_user(self.client).is_authenticated)

    def test_logout(self):

        # login in oldAccount manually
        self.client.login(username="oldAccount", password="oldPassword1")  
        self.assertTrue(auth.get_user(self.client).is_authenticated)

        # execute log out
        response = self.client.post('/accounts/logout/')
        self.assertEqual(response.status_code, 302)

        # check if user logged out
        self.assertFalse(auth.get_user(self.client).is_authenticated)


    # fully uncomment when password change is implemented
    def test_change_password(self):

        self.assertTrue(self.oldUser.check_password('oldPassword1'))

        # login in oldAccount manually
        self.client.login(username="oldAccount", password="oldPassword1")  
        self.assertTrue(auth.get_user(self.client).is_authenticated)

        # change password incorrectly
        self.client.post('/profile/', {'Password':'newPassword1', \
                                       'Confirm Password':'diffPassword1'})
        
        # password should be the same
        self.assertTrue(self.oldUser.check_password('oldPassword1'))

        # change password correctly
        self.client.post('/profile/', {'Password':'newPassord1', \
                                       'Confirm Password':'newPassword1'})

        # password should be different
        #self.assertTrue(self.oldUser.check_password('newPassword10'))

    # fully uncomment when password change is implemented
    def test_forget_password(self):

        self.client.post('/profile/', {'email': 'oldAccount@test.com'})

        #self.assertEqual(len(mail.outbox), 1)
        # ToDo change to correct subject line
        #self.assertTrue(mail.outbox[0].subject == 'Subject here')

        # ToDo change to correct body message
        #self.assertTrue(mail.outbox[0].body == 'Here is the message.')

        # ToDo change to correct outgoing email address
        #self.assertTrue(mail.outbox[0].from_email == 'from@example.com')
        #self.assertTrue(mail.outbox[0].to == ['oldAccount@test.com'])

class TestTripSearch(TestCase):

    def setUp(self):
        self.browser = Browser('chrome')

    def test_search_from_default_screen(self):

        # test Inspire button
        # go to welcome screen
        self.browser.visit('http://127.0.0.1:8000')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that Locations came up
        self.assertFalse(self.browser.find_by_name('set_destination').is_empty())


        # test Inspire button leaving returning field blank
        # go to welcome screen
        self.browser.visit('http://127.0.0.1:8000')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('departure_date', '06-10-2020')

        # press Specify Destination button
        self.browser.find_by_name('without_destination').click()

        # check that user remained on page
        self.assertEqual(self.browser.url, 'http://127.0.0.1:8000/')


        # search for non-existing flight
        # test Inspire Me button
        # go to welcome screen
        self.browser.visit('http://127.0.0.1:8000')

        # fill out destination form
        self.browser.fill('departure', 'HRI')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')

        # press Specify Destination button
        self.browser.find_by_name('without_destination').click()

        # check that no Locations came up
        self.assertTrue(self.browser.find_by_name('set_destination').is_empty())


        # input invalid airport code
        # test Inspire button
        # go to welcome screen
        self.browser.visit('http://127.0.0.1:8000')

        # fill out destination form
        self.browser.fill('departure', 'ZZZ')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that user remained on page
        #self.assertEqual(self.browser.url, 'http://127.0.0.1:8000/')


        # search for existing flight leaving Flying From field blank
        # test Inspire Me button
        # go to welcome screen
        self.browser.visit('http://127.0.0.1:8000')

        # fill out destination form
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that user remained on page
        self.assertEqual(self.browser.url, 'http://127.0.0.1:8000/')


        # search for existing flight leaving the departure time field blank
        # test Inspire Me button
        # go to welcome screen
        self.browser.visit('http://127.0.0.1:8000')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('return_date', '06-24-2020')

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that user remained on page
        self.assertEqual(self.browser.url, 'http://127.0.0.1:8000/')

    def test_search_from_welcome_screen(self):

        # test Inspire button
        # go to welcome screen
        self.browser.visit('http://127.0.0.1:8000/welcome')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that Locations came up
        self.assertFalse(self.browser.find_by_name('set_destination').is_empty())


        # test Inspire button leaving returning field blank
        # go to welcome screen
        self.browser.visit('http://127.0.0.1:8000/welcome')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('departure_date', '06-10-2020')

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that user remained on page
        self.assertEqual(self.browser.url, 'http://127.0.0.1:8000/welcome')


        # search for non-existing flight
        # test Inspire Me button
        # go to welcome screen
        self.browser.visit('http://127.0.0.1:8000/welcome')

        # fill out destination form
        self.browser.fill('departure', 'HRI')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that no Locations came up
        self.assertTrue(self.browser.find_by_name('set_destination').is_empty())


        # input invalid airport code
        # test Inspire button
        # go to welcome screen
        self.browser.visit('http://127.0.0.1:8000/welcome')

        # fill out destination form
        self.browser.fill('departure', 'ZZZ')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that user remained on page
        # self.assertEqual(self.browser.url, 'http://127.0.0.1:8000/welcome')


        # search for existing flight leaving Flying From field blank
        # test Inspire Me button
        # go to welcome screen
        self.browser.visit('http://127.0.0.1:8000/welcome')

        # fill out destination form
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that user remained on page
        self.assertEqual(self.browser.url, 'http://127.0.0.1:8000/welcome')


        # search for existing flight leaving the departure time field blank
        # test Inspire Me Destination button
        # go to welcome screen
        self.browser.visit('http://127.0.0.1:8000/welcome')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('return_date', '06-24-2020')

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that a flight came up
        self.assertEqual(self.browser.url, 'http://127.0.0.1:8000/welcome')


    def test_destination(self):

        # search for existing flight
        # test Specify Destination button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('arrival', 'JFK')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '2')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Specify Destination button
        self.browser.find_by_name('with_destination').click()

        # check that a flight came up
        self.assertFalse(self.browser.find_by_name('set_destination').is_empty())


        # search for existing flight, leaving To field blank
        # test Specify Destination button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '2')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Specify Destination button
        self.browser.find_by_name('with_destination').click()

        # check that a flight came up
        self.assertFalse(self.browser.find_by_name('set_destination').is_empty())


        # search for existing flight
        # test Inspire Me button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('arrival', 'JFK')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '2')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Specify Destination button
        self.browser.find_by_name('without_destination').click()

        # check that a flight came up
        self.assertFalse(self.browser.find_by_name('set_destination').is_empty())


        # search for existing flight
        # test Inspire Me button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('departure_date', '06-10-2020')

        # press Specify Destination button
        self.browser.find_by_name('without_destination').click()

        # check that a didn't come up
        self.assertFalse(self.browser.find_by_name('set_destination').is_empty())


        # search for non-existing flight
        # test Specify Destination button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'HRI')
        self.browser.fill('departure_date', '06-14-2020')
        self.browser.fill('return_date', '06-14-2020')

        # press Specify Destination button
        self.browser.find_by_name('with_destination').click()

        # check that no flights came up
        self.assertTrue(self.browser.find_by_value('Add Flight to Trip').is_empty())


        # search for non-existing flight
        # test Inspire Me button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'HRI')
        self.browser.fill('departure_date', '06-14-2020')
        self.browser.fill('return_date', '06-14-2020')

        # press Specify Destination button
        self.browser.find_by_name('without_destination').click()

        # check that the correct flight came up
        self.assertTrue(self.browser.find_by_name('set_destination').is_empty())

        
        # input invalid airport code
        # test Specify Destination button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'ZZZ')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')

        # press Specify Destination button
        self.browser.find_by_name('with_destination').click()

        # check that user remained on page
        #self.assertEqual(self.browser.url, 'http://127.0.0.1:8000/')


        # input invalid airport code
        # test Inspire button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'ZZZ')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')

        # press Specify Destination button
        self.browser.find_by_name('without_destination').click()

        # check that user remained on page
        #self.assertEqual(self.browser.url, 'http://127.0.0.1:8000/')


        # search for existing flight leaving Flying From field blank
        # test Specify Destination button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('arrival', 'JFK')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '2')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Specify Destination button
        self.browser.find_by_name('with_destination').click()

        # check that user remained on page
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')


        # search for existing flight leaving Flying From field blank
        # test Inspire Me button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('arrival', 'JFK')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '2')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Specify Destination button
        self.browser.find_by_name('without_destination').click()

        # check that user remained on page
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')


        # search for existing flight leaving the departure time field blank
        # test Specify Destination button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('arrival', 'JFK')
        self.browser.fill('departure_date', '')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '2')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Specify Destination button
        self.browser.find_by_name('with_destination').click()

        # check that user remained on page
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')


        # search for existing flight leaving the departure time field blank
        # test Inspire Me button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('arrival', 'JFK')
        self.browser.fill('departure_date', '')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '2')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that user remained on page
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')


        # search for existing flight leave number of travelers field blank
        # test Specify Destination button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('arrival', 'JFK')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Specify Destination button
        self.browser.find_by_name('with_destination').click()

        # check that a flight came up
        self.assertFalse(self.browser.find_by_name('set_destination').is_empty())


        # search for existing flight leave number of travelers field blank
        # test Inspire Me button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('arrival', 'JFK')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that a flight came up
        self.assertFalse(self.browser.find_by_name('set_destination').is_empty())


        # search for existing flight enter negative value for number of travelers
        # test Specify Destination button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('arrival', 'JFK')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '-1')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Specify Destination button
        self.browser.find_by_name('with_destination').click()

        # check that a flight came up
        self.assertFalse(self.browser.find_by_name('set_destination').is_empty())


        # search for existing flight
        # test Inspire Me button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('arrival', 'JFK')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '-1')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that a flight came up
        self.assertFalse(self.browser.find_by_name('set_destination').is_empty())


        # search for existing flight enter non-integer value for number of travelers
        # test Specify Destination button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('arrival', 'JFK')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '3.5')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Specify Destination button
        self.browser.find_by_name('with_destination').click()

        # check that a flight came up
        self.assertFalse(self.browser.find_by_name('set_destination').is_empty())


        # search for existing flight enter non-integer value for number of travelers
        # test Inspire Me button
        # go to destination screen
        self.browser.visit('http://127.0.0.1:8000/destination?departure=SAN&departure_date=2020-06-10&return_date=2020-06-28')

        # fill out destination form
        self.browser.fill('departure', 'SAN')
        self.browser.fill('arrival', 'JFK')
        self.browser.fill('departure_date', '06-10-2020')
        self.browser.fill('return_date', '06-24-2020')
        self.browser.find_by_name('daily_budget').first.select('value_midrange')
        self.browser.find_by_name('region').first.select("NA")
        self.browser.find_by_name('activity').first.select("shopping")
        self.browser.fill('travelers', '3.5')
        self.browser.find_by_name('priority').first.select("cheapest")

        # press Inspire Me button
        self.browser.find_by_name('without_destination').click()

        # check that a flight came up
        self.assertFalse(self.browser.find_by_name('set_destination').is_empty())