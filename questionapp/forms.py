from django import forms
from .models import Question,Answer,Test,Subject

class QuestionForm(forms.ModelForm):
    '''Form for creating and Question'''
    class Meta:
        model = Question
        fields = '__all__'
        exclude = ('updated',)
        widgets = {
          'question': forms.Textarea(attrs={'rows':3, 'cols':15}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'
        exclude = ('question',)

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
        exclude = ('updated','created_by','questions')

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"

