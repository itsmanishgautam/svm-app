# from django.contrib import admin
from django.urls import path
from dashboard import views
app_name = 'dashboard'
urlpatterns = [
    # path('dashboard/', ),
    path("",views.home,name='home'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('signup/',views.signupPage,name='signup'),
    path('take_test/',views.test_index,name='take_test_index'),
    path('take_test/<int:test_id>/',views.testPage,name='taketest'),
    path('questionpool/',views.list_questions,name='questionpool'),
    path('edit_question/<int:question_id>/',views.question_edit,name='edit_question'),
    path('manage_option/<int:question_id>/',views.manage_option,name='manage_option'),
    path('add_option/<int:question_id>/',views.add_option,name='add_option'),
    path('edit_option/<int:option_id>/',views.edit_option,name='edit_option'),
    path('delete_option/<int:option_id>/',views.delete_option,name='delete_option'),
    path('list_test/',views.list_test,name='list_test'),
    path('add_test/',views.add_test,name='add_test'),
    path('edit_test/<int:test_id>/',views.edit_test,name='edit_test'),
    path('questionstatics/',views.questionstatics,name='questionstatics'),
    path('questionaddtest/<int:test_id>/',views.question_add,name="question_add"),
    path('upload_csv/',views.UploadCsv.as_view(),name='upload_csv'),
    path('addquestiontotest/<int:test_id>/',views.AddQuestionsToTestAPIView.as_view(),name="addquestiontotest"),
    path('test_attempts/',views.view_test_attempts,name='test_attempts'),
    path('test_attempts_by_test/<int:test_id>/',views.view_test_attempts_by_test,name='test_attempts_by_test'),

    path('view_test_questions/<int:test_id>/',views.view_test_questions,name="view_test_questions"),

    path('list_subject/',views.list_subject,name='list_subject'),
    path('create_subject/',views.create_subject,name="create_subject"),


    path('download_csv_sample/',views.download_csv,name="download_csv"),
    path('view_users/',views.list_users,name='view_users'),
]   