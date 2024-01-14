from django.urls import path
from .views import all_questions, question_detail, ask, QuestionUpdateView, delete_question, like_view


app_name = 'base'

urlpatterns = [
    path('', all_questions, name='all_questions'),
    path('<slug:slug>/', question_detail, name='question_detail'),
    path('/ask/', ask, name="ask"),
    path('question/<slug:slug>/update/', QuestionUpdateView.as_view(), name='question_update'),
    path('question/<slug:slug>/delete/', delete_question, name='delete_question'),
    path('like/<int:pk>' , like_view, name='like_post'),
  

]


