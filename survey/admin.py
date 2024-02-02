from django.contrib import admin
from django.contrib.auth.models import Group

from survey.models import Answer, Question, Survey, UserAnswer


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('respondents',)


class AnswerInline(admin.TabularInline):
    model = Answer
    fk_name = 'question'
    min_num = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey', 'is_first')
    inlines = [
        AnswerInline,
    ]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'next_question')


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer')


admin.site.unregister(Group)
