import datetime
from django.utils import timezone
from django.test import TestCase

from .models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        should return false if published in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        should return true if published in the last month
        """
        time = timezone.now() - datetime.timedelta(hours =23)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_old_question(self):
        """
        should return false if
        """
        time = timezone.now() - datetime.timedelta(days=1000)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)
