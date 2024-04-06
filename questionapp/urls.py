from django.urls import path
from questionapp import views

urlpatterns = [
    path('question/',views.questionPage,name='questionpage'),
    path('getnextquestion/<int:test_id>/',views.GetQuestionView.as_view(),name="getquestionview"),
    path('submitquestionattempt/',views.QuestionSubmissionView.as_view(),name='submitquestionattempt'),
    path('questionlist/',views.QuestionListView.as_view(),name='questionlist')
]