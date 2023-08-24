from django.urls import path

from . import views

app_name = "polls"
# url에 걸리면 view를 보여줌(views.py에서 해당하는 view로 연결)
# path 안의 url은 장고에서 지원해주는 패턴
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]