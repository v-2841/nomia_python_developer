from django.contrib import admin
from django.contrib.auth.models import Group

from surveys.models import Answer, Question, Survey, UserAnswer, UserSurvey


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['first_question'].queryset = Question.objects.filter(
            survey=obj)
        return form


class AnswerInline(admin.TabularInline):
    model = Answer
    fk_name = 'question'
    min_num = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey')
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'next_question')


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer')


@admin.register(UserSurvey)
class UserSurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey')


admin.site.unregister(Group)
