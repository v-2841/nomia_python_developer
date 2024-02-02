from django.db import models
from django.contrib.auth.models import User


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
    respondents = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Количество респондентов',
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
    is_first = models.BooleanField(
        default=False,
        verbose_name='Первый вопрос',
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
        return self.text


class UserAnswer(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='answers',
        verbose_name='Пользователь',
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

    def __str__(self):
        return self.user
