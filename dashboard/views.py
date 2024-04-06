from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from questionapp.models import Question,Answer,Test,UserQuestionAttempt,TestAttempt,Subject
from questionapp.forms import QuestionForm,AnswerForm,TestForm,SubjectForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout,password_validation
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from django.utils import timezone
from django.urls import reverse
import csv
from questionapp.forms import QuestionForm,AnswerForm

from django.db.models import Avg, Count, Q,Max

from .forms import UserRegistrationForm
# Create your views here.
from django.contrib.auth import get_user_model
User = get_user_model()



@login_required()
def list_users(request):
    users = User.objects.all()
    context = {
        'users':users
    }
    return render(request,'dashboard/list_users.html',context)

@login_required()
def home(request):
    questionss = Question.objects.all()
    if request.user.is_staff:
        test_attempts = TestAttempt.objects.all()
        user_test_attempts_count = test_attempts.count()
        user_incomplete_tests_count = test_attempts.filter(completed=False).count()
        user_completed_tests_count = test_attempts.filter(completed = True).count()
        total_questions = questionss.count()
        easy_count = questionss.filter(category="EASY").count()
        hard_count = questionss.filter(category="HARD").count()
        uncategorized  = questionss.filter(category="UNCATEGORIZED").count()
        mero_attempt = TestAttempt.objects.filter(user=request.user)
        attempt_count = mero_attempt.count()
        incomplete_attempts = mero_attempt.filter(completed=False).count()
        completed_attempts = mero_attempt.filter(completed=True).count()
    else:
        test_attempts = TestAttempt.objects.filter(user=request.user)
        attempt_count = test_attempts.count()
        incomplete_attempts = test_attempts.filter(completed=False).count()
        completed_attempts = test_attempts.filter(completed=True).count()
        easy_count = None
        hard_count =None
        uncategorized = None
        user_test_attempts_count = None
        user_completed_tests_count = None
        user_incomplete_tests_count = None
        total_questions =None
        
    context = {
        'user_test_attempts_count':user_test_attempts_count,
        'user_completed_test_count':user_completed_tests_count,
        'user_incomplete_test_count':user_incomplete_tests_count,
        'easy_count':easy_count,
        'hard_count':hard_count,
        'uncategorized':uncategorized,
        'questions_count':total_questions,
        'attempt_count':attempt_count,
        'incomplete_attempts':incomplete_attempts,
        'completed_attempts':completed_attempts,


    }
    return render(request,'dashboard/dashboard.html',context)

@login_required()
def testPage(request,test_id):
    context = {
        'test_id':test_id
    }
    return render(request,'dashboard/testpage.html',context)


@login_required()
def logoutPage(request):
    logout(request)
    messages.info(request,"Logout Successfully")
    return redirect('dashboard:login')


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard:home')
        else:
            messages.info(request,"Username or Password Incorrect")
   
    context ={
    
    }
    return render(request,'login.html',context)

def signupPage(request):
    if request.method == 'POST':
        first_name  = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        form  = UserRegistrationForm(request.POST)
        # if form.is_vaild():
        if first_name is not None and last_name is not None and username is not None and password is not None :
        
            if not User.objects.filter(username__iexact=username).exists():
        
                if password:
                    try:
                        password_validation.validate_password(password, User)
                    except ValidationError as error:
                        print(error)
                        messages.info(request,''.join(x for x in error))
                    
                        return render(request,'signup.html')     
                user = User.objects.create(username=username,first_name=first_name,last_name=last_name)
                user.set_password(password)
                user.save()


            else:
        
                messages.info(request,f'username {username} already taken')
            
            messages.info(request,"User Registered")
            return redirect('dashboard:login')
        else:
            messages.info(request,'Please correct errors!')


    context = {}
    # print('default-signup')
    return render(request,'signup.html',context)

@login_required()
def list_questions(request):
    form = QuestionForm()
    if request.method == "POST":
        print(request.POST)
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:questionpool')

    questions = Question.objects.all().prefetch_related('answers').order_by('-updated')
    questions_count = questions.count()
    easy_count = questions.filter(category='EASY').count()
    hard_count = questions.filter(category="HARD").count()
    
    context = {
        'questions':questions,
        'questions_count':questions_count,
        'easy_count':easy_count,
        'hard_count':hard_count,
        'form':form
    }

    return render(request,'dashboard/list_questions.html',context)


@login_required()    
def list_test(request):
    tests = Test.objects.all()
    form = TestForm()
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            test.save()
            return redirect('dashboard:list_test')
        
    context = {
        'tests':tests,
        'form':form
    }
    return render(request,'dashboard/list_test.html',context)


@login_required()
def add_test(request):
    form = TestForm()
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            test.save()
            return redirect('dashboard:list_test')
        
    context = {
        'form':form
    }
    return render(request,'dashboard/add_test.html',context)

def edit_test(request,test_id):
    
    test = Test.objects.get(id=test_id)

    form = TestForm(instance=test)
    if request.method == "POST":
        form = TestForm(request.POST,instance=test)
        if form.is_valid():
            form.save()
            return redirect('dashboard:list_test')
    context = {
        'test':test,
        'form':form
    }
    return render(request,'dashboard/edit_test.html',context)


@login_required()
def test_index(request):
    # tests = Test.objects.all().prefetch_related('test_attempts')

    tests_with_attempt_count = Test.objects.filter(status='LIVE').prefetch_related('test_attempts').annotate(
    num_attempts=Count('test_attempts', filter=Q(test_attempts__user__id=request.user.id)),
    max_score = Max('test_attempts__score',filter=(Q(test_attempts__user=request.user)&Q(test_attempts__completed=True)))
    )
    # for test in tests_with_attempt_count:
    #     print("Num of attempts: ",test.num_attempts)
    #     print("Max Score: ",test.max_score)
    context = {
        'tests':tests_with_attempt_count
    }
    return render(request,'dashboard/take_test_index.html',context)


from aiquiz.svm_classifier import ModelPredict
@login_required()
def questionstatics(request):
    question_stats = UserQuestionAttempt.objects.filter(
    question__in=Question.objects.all()

    ).values(
        'question'
    ).annotate(
        avg_time=Avg('time_taken'),
        num_attempts=Count('question'),
        num_right_attempts=Count('question', filter=Q(right_attempt=True))
    )
    print(question_stats)

    data = {
    'question_id': [],
    'AverageTimeTaken': [],
    'NumAttempts': [],
    'NumCorrectAttempts': []
}

    for item in question_stats:
        data['question_id'].append(item['question'])
        data['AverageTimeTaken'].append(item['avg_time'])
        data['NumAttempts'].append(item['num_attempts'])
        data['NumCorrectAttempts'].append(item['num_right_attempts'])
    print(data)
    predections,question_id = ModelPredict(data)
    for predection,qn_id in zip(predections,question_id):
        question = Question.objects.get(id=qn_id)
        if not question.category == predection.upper():
            question.category = predection.upper()
            question.updated = timezone.now()
            question.save()
    # return HttpResponse('lo')
    return redirect('dashboard:questionpool')

@login_required()
def question_add(request,test_id):
    test = Test.objects.get(id=test_id)
    question_count = test.questions.count()
    context = {
        'test_id':test_id,
        'question_count':question_count
    }
    return render(request,'dashboard/question_add_test.html',context)

def question_edit(request,question_id):
    question = Question.objects.get(id=question_id)
    question_form = QuestionForm(instance = question)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST,instance = question)
        if question_form.is_valid():
            question_form.save()
            return redirect('dashboard:questionpool')
    context = {
        'question':question,
        'question_form':question_form
    }
    return render(request,'dashboard/question_edit.html',context)


def create_subject(request):
    form = SubjectForm()
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:list_subject')
        
    context = {
        'form':form
    }
    return render(request,'dashboard/subject/addsubject.html',context)

def list_subject(request):
    subjects = Subject.objects.all()

    context  = {
        'subjects':subjects
    } 

    return render(request,'dashboard/subject/list_subject.html',context)

def view_test_questions(request,test_id):
    test = Test.objects.get(id=test_id)
    questions = test.questions.all().select_related('subject')
    context = {
        'test':test,
        'questions':questions
    }
    return render(request,'dashboard/view_test_questions.html',context)

@login_required()
def manage_option(request,question_id):
    question = Question.objects.get(id=question_id)
    form  = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_id = question_id
            answer.save()
            return redirect(reverse('dashboard:manage_option',kwargs={'question_id': question_id}))
    
    context = {
        'question':question,
        'form':form
    } 
    return render(request,'dashboard/manage_option.html',context)



def edit_option(request,option_id):
    option = Answer.objects.get(id=option_id)
    form = AnswerForm(instance=option)
    if request.method == "POST":
        form = AnswerForm(request.POST,instance=option)
        if form.is_valid():
            answer_obj = form.save()
            return redirect(reverse('dashboard:manage_option',kwargs={'question_id':answer_obj.question.id}))
    context = {
        'option':option,
        'form':form
    }
    return render(request,'dashboard/edit_option.html',context)
def delete_option(request,option_id):
    option = Answer.objects.get(id=option_id)
    option.delete()
    return redirect(reverse('dashboard:manage_option',kwargs={'question_id':option.question.id}))
    
def add_option_by_question(request,question_id):
    question = Question.objects.get(id=question_id)
    form  = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_id = question_id
            answer.save()
            return redirect(reverse('dashboard:manage_option',kwargs={'question_id': question_id}))
    
    context = {
        'question':question,
        'form':form
    } 

    return render(request,'dashboard/add_option.html',context)

@login_required()
def add_option(request,question_id):
    form  = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_id = question_id
            answer.save()
            return redirect('dashboard:questionpool')
    question = Question.objects.get(id=question_id)
    context = {
        'question':question,
        'form':form
    } 

    return render(request,'dashboard/add_option.html',context)

def download_csv(request):
    # Create a response object with the appropriate content type for CSV
    response = HttpResponse(content_type='text/csv')
    
    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = 'attachment; filename="sample_csv_question_file.csv"'

    # Create a CSV writer using the response object
    csv_writer = csv.writer(response)

    # Write your CSV data to the response
    # For example, you can write a list of rows:
    csv_writer.writerow(['id', 'question', 'option1','option2','option3','option4','right_option','subject'])
    csv_writer.writerow(['1', 'Django is the web framework of?', 'Java','Javascript','Python','C++','Python','Web Development'])
    csv_writer.writerow(["2","We can build Android Apps using?","Java","Python","C","Swift","Java","App Development"])
    # ... add more rows as needed

    return response
class UploadCsv(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        file_obj = request.FILES.get('csv_file')  # 'csv_file' should match the field name in the FormData

        if not file_obj:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            print('hello')
            decoded_file = file_obj.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)
            headers = next(csv_reader)  # Skipping headers if present
            new_subjects =[]
            for row in csv_reader:
            
                # Assuming the CSV columns are: ID, Question, Option1, Option2, Option3, Option4, Right Option,Subject
                    question_id = int(row[0])
                    question_text = row[1]
                    # option_length = row[2] 
                    option_length = 4
                    right_option = row[6]
                    # right_option = row[3] 
                    # options = row[4:8]
                    option_ends = 2 + int(option_length) # Assume 2 be the first option position
                    options = row[2:option_ends]


                    print(question_text)
                    print(options)
                    subject = row[7]
                    if subject is not None and subject !="":
                        subject ,created = Subject.objects.get_or_create(name=subject)
                        if created:
                            new_subjects.append(subject.name)
                            print(f"New Subject - {subject.name} Created")

                    # question_obj = Question(question=question_text)
                    # question,created = Question.objects.get_or_create(
                    #     # id=question_id,
                    #     defaults={
                    #         'question': question_text,
                    #         # Adjust other fields as needed
                    #     }
                    # )
                    question = Question.objects.create(question=question_text,subject=subject)

                    for idx, option_text in enumerate(options):
                            
                        print(idx,option_text,(option_text == right_option))
                        Answer.objects.create(
                            question=question,
                            answer=option_text,
                            is_right=(option_text == right_option)  # First option is considered the correct answer
                        )
            
            return JsonResponse({'message': f'Data inserted successfully - New Subjects:{new_subjects}'})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class AddQuestionsToTestAPIView(APIView):
    def post(self, request, test_id):
        test = get_object_or_404(Test, pk=test_id)
        
        question_ids = request.data.get('question_ids', [])  # Assuming you pass question_ids in request data
        print(question_ids)
        # Adding questions to the test
        questions_to_add = Question.objects.filter(pk__in=question_ids)
        test.questions.add(*questions_to_add)
        test.save()

        # serializer = TestSerializer(test)
        return Response({'message':'Questions Added'}, status=status.HTTP_200_OK)

@login_required()
def view_test_attempts(request):
    test_attempts = TestAttempt.objects.filter(user=request.user).order_by('-id')
    context = {
        'test_attempts':test_attempts
    }
    return render(request,'dashboard/test_attempts.html',context)


@login_required()
def view_test_attempts_by_test(request,test_id):
    test_attempts = TestAttempt.objects.filter(user= request.user , test__id = test_id).order_by('-id')
    test = Test.objects.get(id=test_id)
    print(test_attempts)
    context = {
        'test':test,
        'test_attempts':test_attempts
    }
    return render(request,'dashboard/test_attempts_index.html',context)