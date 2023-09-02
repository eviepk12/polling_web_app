from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

import datetime

from .models import Question

def create_question(question_text, days):
    """
        Create a question with the given text and date offset to the current date
        (minus for questions from the past, and positive for questions yet to be published in the future)
    """
    time = timezone.now() - datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """
            If no questions exist, gives the appropriate message
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Polls are available at the moment.")
        self.assertQuerysetEqual(response.context["latest_qustion_list"], [])
    
    def test_past_questions(self):
        """
            Questions with a date from the past will be displayed normally
        """
        question = create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [question]
        )
    
    def test_future_question(self):
        """
            Question with a date from the future won't be displayed in index
        """
        create_question(question_text="Future Text", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
            Even if both future and past questions exist, past question should only be the one
            that is displayed
        """
        create_question(question_text="Future Text", days=30)
        question = create_question(question_text="Past Text", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_two_past_questions(self):
        """
            Even if both future and past questions exist, past question should only be the one
            that is displayed
        """
        question1 = create_question(question_text="Past Question Text 1", days=-30)
        question2 = create_question(question_text="Past Question Text 2", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [question1, question2])


class QuestionModelTests(TestCase):


    def test_was_published_recently_with_old_question(self):
        """
            was_published_recently() should output false on a question dated behind 1 day
        """

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
            was_published_recently() should output true on a question dated within the last day
        """

        time = timezone.now() - datetime.timedelta(days=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_future_question(self):
        """
            was_published_recently() should output false on a question dated from the future
        """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)