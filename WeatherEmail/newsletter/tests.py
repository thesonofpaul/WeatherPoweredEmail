from django.test import TestCase
from newsletter.models import EmailList, Cities
from django.core.management import call_command

class EmailListMethodTests(TestCase):
    def setUp(self):
        Cities.objects.create(id=1, city='Portland', state='Oregon')
        Cities.objects.create(id=2, city='Seattle', state='Washington')
        EmailList.objects.create(email_address='test1@aol.com', location=Cities.objects.get(id=1))
        EmailList.objects.create(email_address='test2@aol.com', location=Cities.objects.get(id=1))
        EmailList.objects.create(email_address='test3@aol.com', location=Cities.objects.get(id=1))

    def test_change_city(self):
        test_email = EmailList.objects.get(email_address='test1@aol.com')
        self.assertEqual(test_email.location, Cities.objects.get(id=1))
        test_email.location = Cities.objects.get(id=2)
        test_email.save()
        self.assertEqual(test_email.location, Cities.objects.get(id=2))

    def test_print_city(self):
        self.assertEquals(Cities.objects.get(id=1).__str__(), 'Portland, Oregon')
        self.assertEquals(Cities.objects.get(id=2).__str__(), 'Seattle, Washington')

    def tearDown(self):
        EmailList.objects.get(email_address='test1@aol.com').delete()
        Cities.objects.get(id=1).delete()
        Cities.objects.get(id=2).delete()