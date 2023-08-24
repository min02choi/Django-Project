# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.template import loader

from django.http import Http404
from django.shortcuts import get_object_or_404, render

from django.views import generic

from django.urls import reverse
from .models import Question, Choice

from django.utils import timezone

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        # __lte(less then equal): 작은것을 가져오게 하는 장고의 내장 함수(필터)
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

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
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    # 데이터가 없는 경우
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render (
            request,
            "polls/detail.html", {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # HttpResponseRedirect는 post와 같이 쓰인다고 보면 됨
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))