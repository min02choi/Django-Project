import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

from django.urls import reverse

# TestCode 작성 이유: 내가 원하는 결과값이 나오는지 확인해주는 것
# 기능을 명확하게 해줌

# TestCase를 상속함
class QuestionModelTests(TestCase):

    # 파일명도 tests, 함수 명도 앞머리는 test로 시작할 것
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)     # 미래에 생성한 질문
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)      # False가 나오길 기대함

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))

        # 테스트 메소드들
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])      # 컨택스트가 비어있는지 확인

    # 과거 데이터를 만들고 Question이 존재하는지 확인. 없으면 문제가 있는 것
    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])      # 결과가 있으면 문제가 있음

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        # 두개의 데이터가 기대되어짐
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

# 12:24