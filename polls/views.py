# from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader
from django.shortcuts import render

from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Question

# view: 클라이언트에게서 request를 받고 HttpResponse 메소드로 반환을 해주는 구조
def index(request):
    # return HttpResponse("Hello, world!!!")
    # 질문을 출판 날짜로 정렬하여 5개만 가지고 오겠다.
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # output = ", ".join([q.question_text for q in latest_question_list])
    # template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list
    }
    # return HttpResponse(template.render(context, request))
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    # return HttpResponse("You're looking at question %s." %question_id)
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s." %question_id)
    

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." %question_id)