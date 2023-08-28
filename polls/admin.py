from django.contrib import admin

from .models import Question
from .models import Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3       # 개수를 세개로 제한

class QuestionAdmin(admin.ModelAdmin):
    # column 값 추가(만든 함수인 was_published_recently()도 추가)
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None,                  {'fields': ['question_text']}),
        ('Date information',    {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline]

    list_filter = ['pub_date']              # 필터 기능 추가
    search_fields = ['question_text']       # 검색창이 만들어짐

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)