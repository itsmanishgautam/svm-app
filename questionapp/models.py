from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User  = get_user_model()
# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=50,)

    def __str__(self):
        return self.name
class Question(models.Model): 
    CATEGORY_CHOICES = [('HARD', 'HARD'),('EASY','EASY'),('UNCATEGORIZED','UNCATEGORIZED')]    
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES,blank=True,null=True,default="UNCATEGORIZED")
    subject = models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True,blank=True,related_name='questions')
    question = models.TextField()
    marks = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,null=True,)
    updated = models.DateTimeField(auto_now=True,null=True,) 
    def __str__(self):
        return self.question

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    answer = models.CharField(max_length=300)
    is_right = models.BooleanField(default=False)
    def __str__(self):
        return self.answer
    


class Test(models.Model):
    TEST_STATUS = [
        ('DRAFT','DRAFT'),
        ('LIVE','LIVE')
    ]
    title = models.CharField(max_length=100,null=True,)
    questions = models.ManyToManyField(Question,related_name="tests",blank=True)
    description = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True,null=True,)
    updated = models.DateTimeField(default=timezone.now,null=True,)
    status = models.CharField(max_length=20,choices=TEST_STATUS,default="DRAFT")
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.title

class TestAttempt(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    test = models.ForeignKey(Test,on_delete=models.SET_NULL,null=True,related_name='test_attempts')
    completed = models.BooleanField(default=False)
    score = models.DecimalField(default=0,max_digits=8,decimal_places=2,null=True)
    total_right = models.IntegerField(default=0,null=True)
    total_wrong = models.IntegerField(default=0,null=True)
    total_questions = models.IntegerField(default=0,null=True)
    timetaken = models.DecimalField(default=0,max_digits=10,decimal_places=2,null=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True,)
    updated= models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"#{self.id} {self.user} - {self.test}"
    

class UserQuestionAttempt(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    test_attempt = models.ForeignKey(TestAttempt,on_delete=models.CASCADE,null=True,related_name='questions_attempt')
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='userquestionattempts')
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null=True,blank=True)
    time_taken = models.DecimalField(default=0,max_digits=10,decimal_places=2,null=True) # in seconds
    right_attempt = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} -> {self.right_attempt} -> {self.answer}"
