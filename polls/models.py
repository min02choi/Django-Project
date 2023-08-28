import datetime

from django.db import models
from django.utils import timezone

# model: 데이터베이스의 구조라고 생각하면 됨
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        # Test Code를 통한 버그를 수정함(미래 날짜는 recent가 아닌것이 되도록)
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'   # 필드를 정렬할 때의 기준을 '발행일'로 하겠다
    was_published_recently.boolean = True       # 아이콘 모양으로의 변경
    was_published_recently.short_description = "Published recently?"    # Title을 변경시켜 주는 속성

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
