from django.contrib import admin

from .models import Question, Answer, Test, TestAttempt, UserQuestionAttempt,Subject


admin.site.register(Subject)
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category',
        'question',
        'marks',
        'active',
        'created',
        'updated',
    )
    list_filter = ('active', 'created', 'updated')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'is_right')
    list_filter = ('question', 'is_right')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'created',
        'updated',
        'created_by',
    )
    list_filter = ('created', 'updated', 'created_by')
    raw_id_fields = ('questions',)


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'test', 'completed', 'score', 'timestamp')
    list_filter = ('user', 'test', 'completed', 'timestamp')


@admin.register(UserQuestionAttempt)
class UserQuestionAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'test_attempt',
        'question',
        'answer',
        'time_taken',
        'right_attempt',
    )
    list_filter = (
        'user',
        'test_attempt',
        'question',
        'answer',
        'right_attempt',
    )