
from .models import Question,UserQuestionAttempt
from django.db.models import Avg, Count, Q

def get_question_statics():
    question_stats = UserQuestionAttempt.objects.filter(
        question__in=Question.objects.all()
        ).values(
            'question'
        ).annotate(
            avg_time=Avg('time_taken'),
            num_attempts=Count('question'),
            num_right_attempts=Count('question', filter=Q(right_attempt=True))
        )
    return question_stats