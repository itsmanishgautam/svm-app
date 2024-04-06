from .models import Answer,Question,TestAttempt,UserQuestionAttempt,Subject
from rest_framework import serializers


class RightAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
         'answer',
         'is_right'
        ]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id',
            'name'
        ]
class QuestionSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    answers = RightAnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = [
            'id',
            'category',
            'question','answers','subject'

        ]