from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from model_mommy import mommy

from simplemooc.courses.models import Course

class CourseManagerTestCase(TestCase):

    def setUp(self):
        self.courses_django = mommy.make(
            'courses.Course',
            name='Python na Web com Django', 
            _quantity=10
        )
        
        self.courses_dev = mommy.make(
            'courses.Course',
            name='Python para Devs',
            _quantity=10
        )

        self.client = Client()

    def tearDown(self):
        Course.objects.all().delete()

    def test_course_search(self):
        search_django = Course.objects.search('django')
        self.assertEqual(len(search_django), 10)
        search_devs = Course.objects.search('devs')
        self.assertEqual(len(search_devs), 10)
        search_python = Course.objects.search('python')
        self.assertEqual(len(search_python), 20)