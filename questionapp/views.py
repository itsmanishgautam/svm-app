from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Question,UserQuestionAttempt,TestAttempt,Test
from .serializers import QuestionSerializer
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Count
# Create your views here.
from .question_statics import get_question_statics
@login_required()
def questionPage(request):
    context = {}
    return render(request,'questionapp/questionpage.html',context)


class GetQuestionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, test_id):
        user = request.user
        test = Test.objects.get(id=test_id)
        test_attempt, created = TestAttempt.objects.get_or_create(user=user,completed=False,test = test)
        # Get the list of questions already answered by the user for the given test
        answered_questions_ids = UserQuestionAttempt.objects.filter(
            user=user,
            test_attempt=test_attempt
        ).values_list('question_id', flat=True)

        # Get the next random unanswered question for the user
        # test = Test.objects.get(id=test_id)
        
        # next_question = Question.objects.filter(
        #     test_id=test_id
        # ).exclude(
        question_count = test.questions.all().count()
        next_question = test.questions.all().exclude(
            id__in=answered_questions_ids
        ).order_by('?').first()  # Randomly select one unanswered question

        if next_question is not None:
            serializer = QuestionSerializer(next_question)
        else:
            print('before completed update: ',test_attempt.total_questions)
            answered_questions = UserQuestionAttempt.objects.filter(
            user=request.user,
            test_attempt=test_attempt).select_related('question')
            answered =  answered_questions.aggregate(time_taken = Sum('time_taken'),count = Count('id'),total_marks=Sum('question__marks'))

            score = answered_questions.filter(right_attempt = True).aggregate(total_score = Sum('question__marks'),right_count= Count('id'))
            wrong_count = answered['count'] - score['right_count']
            percentage = (score['total_score']/answered['total_marks'])*100
            print('Question Answered: ',answered['count']
                  ,"time_taken:",answered['time_taken'],
                  'SCORE:',score['total_score'],
                  'RIGHT COUNT: ',score['right_count'],
                  'WRONG: ',wrong_count,'Percentage: ',percentage)
            # percentage = (score['total_score']/answered['total_marks'])*100
            test_attempt.score = percentage
            test_attempt.total_right=score['right_count']
            test_attempt.total_wrong = wrong_count
            test_attempt.total_questions = answered['count']
            test_attempt.timetaken = answered['time_taken']
            test_attempt.completed=True
            test_attempt.save()

            
            #TODO:update User Attempt Marks 
            ''' 
            '''
            # question_stats = get_question_statics()

            # print(question_stats)
            
            return Response({
                'score':test_attempt.score,
                'completed':True,
                'attempt_id':test_attempt.id,
                'message':"Test Completed"
            })
        data = {
            'no_of_questions':question_count,
            'completed':False,
            'attempt_id':test_attempt.id,
            'current_question_sn':answered_questions_ids.count() + 1,
            'question':serializer.data
        }
        return Response(data)


class QuestionSubmissionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request.data)
        test_attempt_id = request.data.get('test_attempt_id')
        userattempt = UserQuestionAttempt(user = request.user,test_attempt_id=request.data['test_attempt_id'],question_id=request.data['question'],answer_id=request.data.get('answer'),time_taken=request.data.get('timetaken'),right_attempt=request.data.get('right_attempt'))
        userattempt.save()
        test_attempt = TestAttempt.objects.get(id=test_attempt_id)
        return Response({'status':'ok',})

class QuestionListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        question_key = request.query_params.get('question')
        if question_key is not None and question_key != "":
            question_list = Question.objects.filter(question__icontains = question_key,active=True)
        else:
            question_list = Question.objects.filter(active=True)
        question_serializer = QuestionSerializer(question_list,many=True)

        print(request.data)
        return Response({
            'questions':question_serializer.data,
            'status':True
        })


