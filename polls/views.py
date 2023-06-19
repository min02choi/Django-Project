# from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

# view: 클라이언트에게서 request를 받고 HttpResponse 메소드로 반환을 해주는 구조
def index(request):
    # return HttpResponse("Hello, world!!!")
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." %question_id)

def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s." %question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." %question_id)