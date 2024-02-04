from django.contrib.auth.models import User
from django.db import models


class Survey(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название опроса',
    )
    description = models.TextField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name='Описание опроса',
    )
    first_question = models.ForeignKey(
        'Question',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Первый вопрос',
        related_name='first_surveys_questions',
    )
    respondents = models.ManyToManyField(
        User,
        through='UserSurvey',
    )

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField(
        max_length=255,
        verbose_name='Текст вопроса',
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Опрос',
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.survey.name} - {self.text}'


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос',
    )
    text = models.TextField(
        max_length=1024,
        verbose_name='Текст ответа',
    )
    next_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Следующий вопрос',
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f'{self.question.text} - {self.text}'


class UserSurvey(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='surveys',
        verbose_name='Пользователь',
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Опрос',
    )
    last_answer = models.ForeignKey(
        Answer,
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Последний ответ',
    )

    class Meta:
        verbose_name = 'Опрос пользователя'
        verbose_name_plural = 'Опросы пользователей'
        constraints = [
            models.UniqueConstraint(fields=['user', 'survey'],
                                    name='unique_user_survey'),
        ]

    def __str__(self):
        return f'{self.user} - {self.survey}'


class UserAnswer(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='answers',
        verbose_name='Пользователь',
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Ответ',
    )

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'],
                                    name='unique_user_question'),
        ]

    def __str__(self):
        return f'{self.user} - {self.question} - {self.answer}'
